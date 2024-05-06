from pathlib import Path
from typing import Optional, Union

import fire

from ocr_and_translate_en2jp.genarate_tranrate_df import df_generator, output_results


def df_generator_wrapper(
    file_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = './',
    output_file_name: str = 'output',
    max_words: Optional[int] = None,
    do_shuffle_output: bool = False,
    seed: Optional[int] = None,
    do_output_csv: Optional[bool] = True,
    do_output_excel: Optional[bool] = False,
    do_clean_noise_data: Optional[bool] = True,
) -> None:
    file_path = Path(file_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = df_generator(
        file_path=file_path,
        max_words=max_words,
        do_shuffle_output=do_shuffle_output,
        seed=seed,
        do_clean_noise_data=do_clean_noise_data,
    )

    output_results(df, output_dir, output_file_name, do_output_csv, do_output_excel)


if __name__ == '__main__':
    fire.Fire(df_generator)
