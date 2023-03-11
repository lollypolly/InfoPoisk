import ru_core_news_md
import nltk
from collections import Counter
import math



nlp = ru_core_news_md.load()
nltk.download('popular')

dict_lemma_index = {}
dict_lemma = {}


def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')):
    return not alphabet.isdisjoint(text.lower())


word_for_remove = ['и', 'или', 'в', 'а', 'из-за', 'из-под', 'над', 'да', 'если', 'что', 'когда', 'потому', 'зато',
                   'однако', 'либо', 'не', 'то', 'лишь', 'едва', 'так', 'же', 'также', 'ни', 'с', 'где', 'на',
                   'по', 'из', 'за', 'об', 'под', 'для', 'при']


def matchNotRussian(text, alphabet=set('abcdefghijklmnopqrstuvwxyz123456789\'<">/][-=+_!@#$%^*():;}{|.,`~')):
    return not alphabet.isdisjoint(text.lower())


def read_file_lemmas(tmp_dict, name_of_file):
    with open('/Users/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/Lemmas_And_Tokens/' + name_of_file) as f:
        for line in f:
            (key, val) = line.split(':')
            for s in val.split(','):
                s = s.rstrip()
                if key in tmp_dict:
                    tmp_dict[key].update([s])
                else:
                    tmp_dict[key] = {s}


def analyze_html(index):
    token_idf_tfidf = {}
    lemma_idf_tfidf = {}
    tokens = []
    filename = '/Users/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/indexes/index' + str(index) + '.html'
    print(filename)
    file = open(filename, encoding='utf-8').read()
    tmp_tokens = nltk.word_tokenize(file, language='russian')
    for t in tmp_tokens:
        t = t.lower().strip()
        if match(t) and not matchNotRussian(t) and len(t) >= 2 and t not in word_for_remove:
            tokens.append(t)
    counters_tokens = Counter(tokens)
    lemmas_from_token = []
    for t in tokens:
        lemmas_from_token.append(nlp(t)[0].lemma_)

    counters_lemmas = Counter(lemmas_from_token)

    for key in dict_lemma_index.keys():
        if str(index) in dict_lemma_index[key]:
            all_docs_with_lemma = len(dict_lemma_index[key])
            tmp_idf = math.log10(100 / all_docs_with_lemma)
            for t in dict_lemma[key]:
                if t in tokens:
                    tf = counters_tokens[t]/len(tokens)
                    if t in token_idf_tfidf:
                        token_idf_tfidf[t].append(tmp_idf)
                    else:
                        token_idf_tfidf[t] = [tmp_idf]
                    token_idf_tfidf[t].append(tf*tmp_idf)
            lemma_tf = counters_lemmas[key]/len(lemmas_from_token)
            if key in lemma_idf_tfidf:
                lemma_idf_tfidf[key].append(tmp_idf)
            else:
                lemma_idf_tfidf[key] = [tmp_idf]
            lemma_idf_tfidf[key].append(lemma_tf * tmp_idf)

    for key in token_idf_tfidf.keys():
        f = open('/Users/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/Tf-Idf/token-index' + str(index) + '.txt', 'a')
        f.write(key + ' ')
        for t in token_idf_tfidf[key]:
            f.write(str(t) + ' ')
        f.write('\n')
        f.close()

    for key in lemma_idf_tfidf.keys():
        f = open('/Users/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/Tf-Idf/lemma-index' + str(index) + '.txt', 'a')
        f.write(key + ' ')
        for t in lemma_idf_tfidf[key]:
            f.write(str(t) + ' ')
        f.write('\n')
        f.close()


read_file_lemmas(dict_lemma_index, 'inverted_lemmas.txt')
read_file_lemmas(dict_lemma, 'lemmas.txt')

for i in range(1, 101):
    analyze_html(i)
