from pathlib import Path
from typing import Optional, Union

import fire
import pandas as pd

from ocr_and_translate_en2jp.ocr import ocr_image
from ocr_and_translate_en2jp.translate import generate_jp_word_type, translate_word


def df_generator(
    file_path: Optional[Union[str, Path]] = '',
    output_dir: Optional[Union[str, Path]] = './',
    output_file_name: Optional[str] = 'output',
    max_words: Optional[int] = None,
    do_shuffle_output: Optional[bool] = False,
    seed: Optional[int] = None,
    do_output_csv: Optional[bool] = True,
    do_output_excel: Optional[bool] = False,
    do_clean_noise_data: Optional[bool] = True,
) -> None:
    ocr_result = ocr_image(file_path, is_return_list=True)
    ocr_result = list(set(ocr_result))
    df = pd.DataFrame(ocr_result, columns=['word'])
    if do_clean_noise_data:
        df = df[df['word'].str.contains('[a-zA-Z]', na=False)].reset_index(drop=True)
    df['word_pos'] = df['word'].apply(generate_jp_word_type)
    if do_clean_noise_data:
        df = df[df['word_pos'].notnull()].reset_index(drop=True)
    df['word_JP'] = df['word'].apply(translate_word)
    if do_clean_noise_data:
        df = df[df['word_JP'].notnull()].reset_index(drop=True)

    if max_words is None:
        max_words = len(df)
    if do_shuffle_output:
        df = df.sample(n=max_words, random_state=seed, ignore_index=True)
    else:
        df = df.head(max_words)
    if do_output_csv:
        output_path = f'{output_dir}/{output_file_name}.csv'
        df.to_csv(output_path, index=False)
    if do_output_excel:
        output_path = f'{output_dir}/{output_file_name}.xlsx'
        df.to_excel(output_path, index=False)


if __name__ == '__main__':
    fire.Fire(df_generator)
