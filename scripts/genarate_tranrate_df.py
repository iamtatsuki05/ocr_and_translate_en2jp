from pathlib import Path
from typing import Optional, Union

import fire
import pandas as pd

from ocr_and_translate_en2jp.ocr import ocr_image
from ocr_and_translate_en2jp.translate import generate_jp_word_type, translate_word


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['word'].str.contains('[a-zA-Z]', na=False)].reset_index(drop=True)
    df['word_pos'] = df['word'].apply(generate_jp_word_type)
    df = df[df['word_pos'].notnull()].reset_index(drop=True)
    df['word_JP'] = df['word'].apply(translate_word)
    return df[df['word_JP'].notnull()].reset_index(drop=True)


def output_results(df: pd.DataFrame, output_dir: Path, output_file_name: str, do_output_csv: bool, do_output_excel: bool) -> None:
    if do_output_csv:
        output_path = output_dir / f'{output_file_name}.csv'
        df.to_csv(output_path, index=False)
    if do_output_excel:
        output_path = output_dir / f'{output_file_name}.xlsx'
        df.to_excel(output_path, index=False)


def df_generator(
    file_path: Optional[Union[str, Path]] = None,
    output_dir: Optional[Union[str, Path]] = './',
    output_file_name: str = 'output',
    max_words: Optional[int] = None,
    do_shuffle_output: bool = False,
    seed: Optional[int] = None,
    do_output_csv: bool = True,
    do_output_excel: bool = False,
    do_clean_noise_data: bool = True,
) -> None:
    ocr_result = list(set(ocr_image(file_path, is_return_list=True)))
    df = pd.DataFrame(ocr_result, columns=['word'])

    if do_clean_noise_data:
        df = clean_data(df)

    max_words = max_words or len(df)
    df = df.sample(n=max_words, random_state=seed, ignore_index=True) if do_shuffle_output else df.head(max_words)

    output_dir = Path(output_dir)
    output_results(df, output_dir, output_file_name, do_output_csv, do_output_excel)


if __name__ == '__main__':
    fire.Fire(df_generator)
