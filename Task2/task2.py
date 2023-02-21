from bs4 import BeautifulSoup
import spacy
import ru_core_news_md

nlp = ru_core_news_md.load()

tokens = set()


def read_html(file_name):
    file = open(file_name, encoding='utf-8').read()
    document = nlp(file)

    for token in document:
        if match(token.lemma_.lower()) and len(token.lemma_.lower()) > 3 and not matchNotRussian(token.lemma_.lower()):
            tokens.add(token.lemma_)
            # print(token.lemma_)


def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')):
    return not alphabet.isdisjoint(text.lower())


def matchNotRussian(text, alphabet=set('abcdefghijklmnopqrstuvwxyz123456789<">/][-=+_!@#$%^*():;}{|.,`~')):
    return not alphabet.isdisjoint(text.lower())


read_html('../indexes/index1.html')
for token in tokens:
    print(token)
