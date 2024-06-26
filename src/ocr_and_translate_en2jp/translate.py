from typing import Final, Optional

import requests
from bs4 import BeautifulSoup

BASE_URL: Final[str] = 'https://ejje.weblio.jp/content/'
WORD_TYPE_JAPANESE_HTML_CLASS: Final[str] = 'content-explanation'
TRANSLATION_HTML_CLASS: Final[str] = 'content-explanation ej'


def generate_soup_from_url(word: str) -> BeautifulSoup:
    response = requests.get(BASE_URL + word)
    return BeautifulSoup(response.text, 'html.parser')


def get_text_from_class(soup: BeautifulSoup, class_name: str) -> Optional[str]:
    try:
        return soup.find(class_=class_name).get_text().strip()
    except AttributeError:
        return None


def get_word_type_japanese(word: str) -> Optional[str]:
    soup = generate_soup_from_url(word)
    text = get_text_from_class(soup, WORD_TYPE_JAPANESE_HTML_CLASS)
    return text.split(' ')[0] if text else None


def get_translation(word: str) -> Optional[str]:
    soup = generate_soup_from_url(word)
    return get_text_from_class(soup, TRANSLATION_HTML_CLASS)


def translate_english_to_japanese(word: str) -> dict[str, Optional[str]]:
    japanese_word_type = get_word_type_japanese(word)
    japanese_translation = get_translation(word)
    return {
        'word': word,
        'japanese_word': japanese_translation,
        'word_type': japanese_word_type,
    }
