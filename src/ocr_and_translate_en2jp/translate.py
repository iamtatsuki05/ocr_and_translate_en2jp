import requests
from bs4 import BeautifulSoup

url = "https://ejje.weblio.jp/content/"


def generate_jp_word_type(word):
    response = requests.get(url + word)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        result = soup.find(class_="KnenjSub").get_text().strip().split(" ")
    except AttributeError:
        result = None
    return result[0]


def translate_word(word):
    response = requests.get(url + word)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        result = soup.find(class_="content-explanation ej").get_text().strip()
    except AttributeError:
        result = None
    return result


def translate_en2jp(word):
    jp_pos = generate_jp_word_type(word)
    japanese_word = translate_word(word)
    properties = {"word": word, "japanese_word": japanese_word, "word_type": jp_pos}
    return properties
