dict_lemma = {}
with open('/home/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/Lemmas_And_Tokens/lemmas.txt') as f:
    for line in f:
        (key, val) = line.split(':')
        for s in val.split(','):
            if key in dict_lemma:
                dict_lemma[key].append(s.rstrip())
            else:
                dict_lemma[key] = [s.rstrip()]

