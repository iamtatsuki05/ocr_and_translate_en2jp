from pathlib import Path
from typing import Final, Optional, Union

from pdf2image import convert_from_path
from PIL import Image
from pytesseract import pytesseract

pytesseract.tesseract_cmd = '/usr/bin/tesseract'

PICTURE_EXTENSIONS: Final[list[str]] = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']


def load_file(file_path: Union[str, Path]) -> Optional[Union[Image.Image, list]]:
    file_path = Path(file_path)
    file_extension = file_path.suffix
    if file_extension == '.pdf':
        return convert_from_path(str(file_path))
    elif file_extension in PICTURE_EXTENSIONS:
        return [Image.open(str(file_path))]
    return None


def ocr_image(
    file_path: Union[str, Path], is_return_list: Optional[bool] = False
) -> Union[str, list]:
    images = load_file(file_path)
    if images is None:
        return []
    ocr_result = ''.join(
        pytesseract.image_to_string(img, lang='eng+jpn') for img in images
    )
    return ocr_result.split() if is_return_list else ocr_result
