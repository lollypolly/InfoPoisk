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
                    dict_lemma_index[key] = set([index])


for i in range(1, 3):
    get_token_in_index(i)


print(dict_lemma_index)