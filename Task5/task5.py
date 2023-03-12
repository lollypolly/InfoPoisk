from flask import Flask, render_template, request
import ru_core_news_md

nlp = ru_core_news_md.load()
dict_lemma_index = {}
dict_lemma = {}
dict_idf = {}
dict_index = {}
result_index = {}


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
            if word in result_index:
                result_index[word].append('index' + str(i))
            else:
                result_index[word] = ['index' + str(i)]


def analyze_input(all_index, splitted_text):
    prev_val = set()
    for i in range(0, len(splitted_text)):
        if splitted_text[i] == 'AND':
            if len(prev_val) != 0:
                print('prev_val  ' + str(prev_val) + '\n')
                print('all_index[splitted_text[i + 1]]    ' + str(all_index[splitted_text[i + 1]]) + '\n')
                prev_val = (list(set(prev_val) & set(all_index[splitted_text[i + 1]])))
            else:
                print('all_index[splitted_text[i - 1]]  ' + str(all_index[splitted_text[i - 1]]) + '\n')
                print('all_index[splitted_text[i + 1]]   ' + str(all_index[splitted_text[i + 1]]) + '\n')
                prev_val.update(list(set(all_index[splitted_text[i - 1]]) & set(all_index[splitted_text[i + 1]])))
        elif splitted_text[i] == 'OR':
            if len(prev_val) != 0:
                print('prev_val  ' + str(prev_val) + '\n')
                print('all_index[splitted_text[i + 1]]    ' + str(all_index[splitted_text[i + 1]]) + '\n')
                prev_val = (list(set(prev_val) | set(all_index[splitted_text[i + 1]])))
            else:
                print('all_index[splitted_text[i - 1]]  ' + str(all_index[splitted_text[i - 1]]) + '\n')
                print('all_index[splitted_text[i + 1]]   ' + str(all_index[splitted_text[i + 1]]) + '\n')
                prev_val.update(list(set(all_index[splitted_text[i - 1]]) | set(all_index[splitted_text[i + 1]])))
        elif splitted_text[i] == 'NOT' and splitted_text[i+1] == 'AND':
            if len(prev_val) != 0:
                print('prev_val  ' + str(prev_val) + '\n')
                print('all_index[splitted_text[i + 1]]    ' + str(all_index[splitted_text[i + 2]]) + '\n')
                prev_val = (list(set(prev_val) - set(all_index[splitted_text[i + 2]])))
            else:
                print('all_index[splitted_text[i - 1]]  ' + str(all_index[splitted_text[i - 2]]) + '\n')
                print('all_index[splitted_text[i + 1]]   ' + str(all_index[splitted_text[i + 2]]) + '\n')
                prev_val.update(list(set(all_index[splitted_text[i - 2]]) - set(all_index[splitted_text[i + 2]])))
        elif splitted_text[i] == 'NOT' and splitted_text[i+1] == 'OR':
            tmp_list = range(1, 101)
            reversed_prev_val = list(set(tmp_list) - set(prev_val))
            if len(prev_val) != 0:
                print('prev_val  ' + str(prev_val) + '\n')
                print('all_index[splitted_text[i + 1]]    ' + str(all_index[splitted_text[i + 2]]) + '\n')
                prev_val = (list(set(reversed_prev_val) | set(all_index[splitted_text[i + 2]])))
            else:
                reversed_val = list(set(tmp_list) - set(all_index[splitted_text[i - 2]]))
                print('all_index[splitted_text[i - 1]]  ' + str(all_index[splitted_text[i - 2]]) + '\n')
                print('all_index[splitted_text[i + 1]]   ' + str(all_index[splitted_text[i + 2]]) + '\n')
                prev_val.update(list(set(reversed_val) - set(all_index[splitted_text[i + 2]])))
    return prev_val


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
    general_output = []
    result_urls = []
    new_splitted_text = []
    if request.method == "GET":
        text = request.values.get('inputtext')
        splitted_text = text.split(' ')
        if len(splitted_text) == 1:
            lemma_word = nlp(text)[0].lemma_
            find_word(lemma_word)
            general_output = result_index[lemma_word]
        elif len(splitted_text) == 0:
            return 'Please! Write smth...'
        else:
            for i in range(0, len(splitted_text)):
                if splitted_text[i] == 'AND' or splitted_text[i] == 'OR' or splitted_text[i] == 'NOT':
                    new_splitted_text.append(splitted_text[i])
                else:
                    new_splitted_text.append(nlp(splitted_text[i])[0].lemma_)

            for i in range(0, len(splitted_text)):
                if splitted_text[i] == 'AND' or splitted_text[i] == 'OR':
                    i += 1
                elif splitted_text[i] == 'NOT':
                    i += 2
                else:
                    find_word(nlp(splitted_text[i])[0].lemma_)

            general_output = list(analyze_input(result_index, new_splitted_text))
        for index in general_output:
            result_urls.append(str(dict_index[index]).replace('[', '').replace(']', '').replace('\\n', '').replace("'", ""))
            print(str(dict_index[index]).replace('[', '').replace(']', '').replace('\\n', ''))

    return render_template('search.html', data=result_urls)


if __name__ == '__main__':
    app.run(debug=True)
