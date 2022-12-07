import pandas as pd
from ocr_and_translate_en2jp.ocr import ocr_image
from ocr_and_translate_en2jp.translate import generate_jp_word_type, translate_word


def df_generator(
    file_path,
    output_dir="./",
    output_name="output",
    max_words=None,
    is_return_shuffle=False,
    seed=None,
    is_return_csv=True,
    is_return_excel=False,
):
    ocr_result = ocr_image(file_path, is_return_list=True)
    ocr_result = list(set(ocr_result))
    df = pd.DataFrame(ocr_result, columns=["word"])
    df["word_pos"] = df["word"].apply(generate_jp_word_type)
    df["word_JP"] = df["word"].apply(translate_word)

    if max_words is None:
        max_words = len(df)
    if is_return_shuffle:
        df = df.sample(n=max_words, random_state=seed, ignore_index=True)
    else:
        df = df.head(max_words)
    if is_return_csv:
        output_path = f"{output_dir}/{output_name}.csv"
        df.to_csv(output_path, index=False)
    if is_return_excel:
        output_path = f"{output_dir}/{output_name}.xlsx"
        df.to_excel(output_path, index=False)


def main():
    df_generator("")


if __name__ == "__main__":
    main()
