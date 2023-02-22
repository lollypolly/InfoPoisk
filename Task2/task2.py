import ru_core_news_md
import nltk

nlp = ru_core_news_md.load()
nltk.download('popular')

tokens = set()
lemmas = set()
word_for_remove = ['и', 'или', 'в', 'а', 'из-за', 'из-под', 'над', 'да', 'если', 'что', 'когда', 'потому', 'зато', 'однако', 'либо', 'не', 'то', 'лишь', 'едва', 'так', 'же', 'также', 'ни', 'с', 'где']


def fill_tokens(file_name):
    print(file_name)
    file = open(file_name, encoding='utf-8').read()
    tmp_tokens = nltk.word_tokenize(file, language='russian')
    for t in tmp_tokens:
        t = t.lower().strip()
        if match(t) and not matchNotRussian(t) and len(t) >= 2 and t not in word_for_remove:
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
