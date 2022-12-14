import os

from pdf2image import convert_from_path
from PIL import Image
from pytesseract import pytesseract


def load_file(file_path):
    file_extension = os.path.splitext(file_path)[-1]
    if file_extension == ".pdf":
        imgs = convert_from_path(file_path)
        return imgs, file_extension
    image_typeList = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    if file_extension in image_typeList:
        return Image.open(file_path, "r"), file_extension
    else:
        return None, None


def ocr_image(file_path, is_return_list=False):
    imgs, data_type = load_file(file_path)
    pytesseract.tesseract_cmd = "/usr/bin/tesseract"
    if data_type == ".pdf":
        ocr_result = ""
        for img in imgs:
            ocr_result += pytesseract.image_to_string(img, lang="eng+jpn")
    else:
        ocr_result = ""
        ocr_result += pytesseract.image_to_string(imgs, lang="eng+jpn")
    if is_return_list:
        return ocr_result.split()
    return ocr_result
