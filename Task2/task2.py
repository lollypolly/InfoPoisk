from bs4 import BeautifulSoup
import spacy
import ru_core_news_md
import nltk

nlp = ru_core_news_md.load()
nltk.download('popular')

tokens = set()
lemmas = set()


def fill_tokens(file_name):
    functors_pos = {'CONJ', 'ADV-PRO', 'CONJ', 'PART'}
    print(file_name)
    file = open(file_name, encoding='utf-8').read()
    tmp_tokens = nltk.word_tokenize(file, language='russian')
    for t in tmp_tokens:
        #https://ru.stackoverflow.com/questions/782994/%D0%A3%D0%B4%D0%B0%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B8%D0%B7-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B8-%D1%81%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D1%8B%D1%85-%D1%87%D0%B0%D1%81%D1%82%D0%B5%D0%B9-%D1%80%D0%B5%D1%87%D0%B8%D1%81%D0%BE%D1%8E%D0%B7%D1%8B-%D0%BF%D1%80%D0%B5%D0%B4%D0%BB%D0%BE%D0%B3%D0%B8-%D1%87%D0%B0%D1%81%D1%82%D0%B8%D1%86%D1%8B-%D0%BC%D0%B5%D0%B6%D0%B4%D0%BE%D0%BC%D0%B5%D1%82%D0%B8%D1%8F-%D0%B8-%D0%B4
        t = t.lower().strip()
        if match(t) and not matchNotRussian(t) and len(t) >= 2:
            tokens.add(t)
            lemmas.add(nlp(t)[0].lemma_)


def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')):
    return not alphabet.isdisjoint(text.lower())


def matchNotRussian(text, alphabet=set('abcdefghijklmnopqrstuvwxyz123456789\'<">/][-=+_!@#$%^*():;}{|.,`~')):
    return not alphabet.isdisjoint(text.lower())


for i in range(1, 101):
    fill_tokens('../indexes/index' + str(i) + '.html')

dict_lemma = {}
fToken = open("../Lemmas_And_Tokens/tokens.txt", "a")
fLemma = open("../Lemmas_And_Tokens/lemmas.txt", "a")

for t in tokens:
    fToken.write(t + '\n')
    new_var = nlp(t)[0].lemma_
    if new_var in dict_lemma:
        dict_lemma[new_var].append(t)
    else:
        dict_lemma[new_var] = [t]
fToken.close()
for key in dict_lemma.keys():
    fLemma.write(key + ':' + ','.join(dict_lemma[key]) + '\n')
fLemma.close()
