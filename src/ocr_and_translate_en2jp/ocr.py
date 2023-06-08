import os
from pathlib import Path
from typing import Optional, Union

from PIL import Image
from pdf2image import convert_from_path
from pytesseract import pytesseract

pytesseract.tesseract_cmd = "/usr/bin/tesseract"


def load_file(file_path: Union[str, Path]) -> Union[Optional[Image.Image], Optional[list]]:
    file_extension = file_path.suffix
    if file_extension == ".pdf":
        return convert_from_path(str(file_path))
    elif file_extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
        return [Image.open(str(file_path))]
    return None


def ocr_image(file_path: Union[str, Path], is_return_list: bool = False) -> Union[str, list]:
    images = load_file(file_path)
    if images is None:
        return []
    ocr_result = "".join(pytesseract.image_to_string(img, lang="eng+jpn") for img in images)
    return ocr_result.split() if is_return_list else ocr_result
