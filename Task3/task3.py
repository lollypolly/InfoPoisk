import ru_core_news_md

nlp = ru_core_news_md.load()

dict_lemma = {}
dict_lemma_index = {}
with open(
        '/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/Lemmas_And_Tokens/lemmas.txt') as f:  # SET PATH TO LEMMAS.TXT
    for line in f:
        (key, val) = line.split(':')
        for s in val.split(','):
            if key in dict_lemma:
                dict_lemma[key].append(s.rstrip())
            else:
                dict_lemma[key] = [s.rstrip()]


def write_to_file_inverted_lemmas():
    lemmas = open("/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/Lemmas_And_Tokens/inverted_lemmas.txt", "a")
    for lemma in dict_lemma_index.keys():
        lemmas.write(lemma + ':')
        tmp_str = ''
        for token in dict_lemma_index[lemma]:
            tmp_str = tmp_str + str(token) + ','
        tmp_str = tmp_str[:-1]
        lemmas.write(tmp_str + '\n')


def read_inverted_lemmas():
    with open('/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/Lemmas_And_Tokens/inverted_lemmas.txt') as f:
        for line in f:
            (key, val) = line.split(':')
            for s in val.split(','):
                s = int(s.rstrip())
                if key in dict_lemma_index:
                    dict_lemma_index[key].update([s])
                else:
                    dict_lemma_index[key] = {s}


def get_token_in_index(index):
    filename = '/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/indexes/index' + str(index) + '.html'
    print(filename)
    file = open(filename, encoding='utf-8').read()
    for key in dict_lemma.keys():
        for token in dict_lemma[key]:
            if token in file:
                if key in dict_lemma_index:
                    dict_lemma_index[key].update([index])
                else:
                    dict_lemma_index[key] = {index}


def bool_and(word1, word2):
    index_from_word1 = dict_lemma_index[nlp(word1)[0].lemma_]
    index_from_word2 = dict_lemma_index[nlp(word2)[0].lemma_]
    general_index = list(set(index_from_word1) & set(index_from_word2))
    print('RESULT OF BOOL_AND')
    print(index_from_word1)
    print(index_from_word2)
    print(general_index)
    for index in general_index:
        print('/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/indexes/index' + str(index) + '.html')


def bool_or(word1, word2):
    index_from_word1 = dict_lemma_index[nlp(word1)[0].lemma_]
    index_from_word2 = dict_lemma_index[nlp(word2)[0].lemma_]
    general_index = list(set(index_from_word1) | set(index_from_word2))

    print('RESULT OF BOOL_OR')
    for index in general_index:
        print('/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/indexes/index' + str(index) + '.html')


def bool_not_and(word1, word2):
    index_from_word1 = dict_lemma_index[nlp(word1)[0].lemma_]
    index_from_word2 = dict_lemma_index[nlp(word2)[0].lemma_]
    general_index = list(set(index_from_word1) - set(index_from_word2))
    print(index_from_word1)
    print(index_from_word2)
    print(general_index)
    print('RESULT OF BOOL_AND')
    for index in general_index:
        print('/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/indexes/index' + str(index) + '.html')


def bool_not_or(word1, word2):
    index_from_word1 = dict_lemma_index[nlp(word1)[0].lemma_]
    index_from_word2 = dict_lemma_index[nlp(word2)[0].lemma_]
    tmp_list = range(1, 101)
    reversed_index_word1 = list(set(tmp_list) - set(index_from_word1))
    general_index = list(set(reversed_index_word1) | set(index_from_word2))
    print(index_from_word1)
    print(index_from_word2)
    print(general_index)
    print('RESULT OF BOOL_AND')
    for index in general_index:
        print('/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/indexes/index' + str(index) + '.html')


# for i in range(1, 101):
#    get_token_in_index(i)
# write_to_file_inverted_lemmas()
### ONLY 1 time run 3 upper string ###
read_inverted_lemmas()

bool_not_or('отношение', 'дух')
