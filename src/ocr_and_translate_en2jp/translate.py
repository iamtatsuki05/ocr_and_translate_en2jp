import sys

from bs4 import BeautifulSoup
import requests
import nltk
nltk.download('averaged_perceptron_tagger')

url='https://ejje.weblio.jp/content/'

def conver_type_en2jp(pos):
    if pos == 'CC':
        jp_pos = '調整接続詞'
    elif pos == 'CD':
        jp_pos = '基数'
    elif pos == 'DT':
        jp_pos = '限定詞'
    elif pos == 'EX':
        jp_pos = '存在を表す there'
    elif pos == 'FW':
        jp_pos = '外国語'
    elif pos == 'IN':
        jp_pos = '前置詞または従属接続詞'
    elif pos == 'JJ':
        jp_pos = '形容詞'
    elif pos == 'JJR':
        jp_pos = '形容詞 (比較級)'
    elif pos == 'JJS':
        jp_pos = '形容詞 (最上級)'
    elif pos == 'LS':
        jp_pos = '-'
    elif pos == 'MD':
        jp_pos = '法'
    elif pos == 'NN':
        jp_pos = '名詞'
    elif pos == 'NNS':
        jp_pos = '名詞 (複数形)'
    elif pos == 'NNP':
        jp_pos = '固有名詞'
    elif pos == 'NNPS':
        jp_pos = '固有名詞 (複数形)'
    elif pos == 'PDT':
        jp_pos = '前限定辞'
    elif pos == 'POS':
        jp_pos = '所有格の終わり'
    elif pos == 'PRP':
        jp_pos = '人称代名詞 (PP)'
    elif pos == 'PRP$':
        jp_pos = '所有代名詞 (PP$)'
    elif pos == 'RB':
        jp_pos = '副詞'
    elif pos == 'RBR':
        jp_pos = '副詞 (比較級)'
    elif pos == 'RBS':
        jp_pos = '副詞 (最上級)'
    elif pos == 'RP':
        jp_pos = '不変化詞'
    elif pos == 'SYM':
        jp_pos = '記号'
    elif pos == 'TO':
        jp_pos = '前置詞 to'
    elif pos == 'UH':
        jp_pos = '感嘆詞'
    elif pos == 'VB':
        jp_pos = '動詞 (原形)'
    elif pos == 'VBD':
        jp_pos = '動詞 (過去形)'
    elif pos == 'VBG':
        jp_pos = '動詞 (動名詞または現在分詞)'
    elif pos == 'VBN':
        jp_pos = '動詞 (過去分詞)'
    elif pos == 'VBP':
        jp_pos = '動詞 (三人称単数以外の現在形)'
    elif pos == 'VBZ':
        jp_pos = '動詞 (三人称単数の現在形)'
    elif pos == 'WDT':
        jp_pos = 'Wh 限定詞'
    elif pos == 'WP':
        jp_pos = 'Wh 代名詞'
    elif pos == 'WP$':
        jp_pos = '所有 Wh 代名詞'
    elif pos == 'WRB':
        jp_pos = 'Wh 副詞'
    else:
        jp_pos = None
    return jp_pos

def generate_jp_word_type(word):
    en_pos = nltk.pos_tag(list(word))[0][-1]
    return conver_type_en2jp(en_pos)

def translate_word(word):
    response = requests.get(url+word)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.find(class_='content-explanation ej').get_text().strip()

def translate_en2jp(word):
    jp_pos = generate_jp_word_type(word)
    japanese_word = translate_word(word)
    properties = {'word': word, 'japanese_word': japanese_word, 'word_type': jp_pos}
    return properties

