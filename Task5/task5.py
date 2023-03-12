from flask import Flask, render_template, request

dict_lemma_index = {}
dict_lemma = {}
dict_idf = {}
dict_index = {}
result_index = []

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

def read_idf(tmp_dict, name_of_file):
    with open('/Users/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/Tf-Idf/' + name_of_file) as f:
        for line in f:
            (key, val) = line.split(' ')
            if key in tmp_dict:
                tmp_dict[key].append(val.split(' ')[0])
            else:
                tmp_dict[key] = [val.split(' ')[0]]
            tmp_dict[key].append(val.split(' ')[1])

def read_index_txt():
    with open('/Users/rinat.r.ahmethanov/PycharmProjects/InfoPoisk/indexes/index.txt') as f:
        for line in f:
            (key, val) = line.split(' - ')
            dict_index[key] = [val]

def find_word(word):
    if word in dict_lemma_index.keys():
        for i in dict_lemma_index[word]:
            result_index.append(dict_index['index' + str(i)][0])



read_file_lemmas(dict_lemma_index, 'inverted_lemmas.txt')
read_file_lemmas(dict_lemma, 'lemmas.txt')
read_index_txt()



app = Flask(__name__, template_folder='./templates')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search/')
def search():
    return render_template('search.html')


@app.route('/make_search/')
def make_search():
    if request.method == "GET":
        text = request.values.get('inputtext')
        find_word(text)
        #print(result_index)
    return result_index


if __name__ == '__main__':
    app.run(debug=True)
