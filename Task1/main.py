from urllib.request import urlopen
from bs4 import BeautifulSoup

default_url = 'https://lenta.ru'
base_urls = ['https://lenta.ru/parts/news/1', 'https://lenta.ru/parts/news/2', 'https://lenta.ru/parts/news/3',
             'https://lenta.ru/parts/news/4', 'https://lenta.ru/parts/news/5', 'https://lenta.ru/parts/news/6',
             'https://lenta.ru/parts/news/7', 'https://lenta.ru/parts/news/8', 'https://lenta.ru/parts/news/9']
all_urls = []
count = 100


def load_page(tmp_url, i):
    print("OPEN URL :" + tmp_url)
    page = urlopen(tmp_url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    f = open("indexes/index" + str(i) + ".html", "w")
    f.write(html)
    f.close()
    f1 = open('indexes/index.txt', 'a')
    f1.write('index' + str(i) + ' - ' + tmp_url + '\n')
    f1.close()


def get_urls_from_page(page):
    soup = BeautifulSoup(page)
    for link in soup.find_all('a', href=True):
        if len(all_urls) >= count:
            return 0
        else:
            if link['href'].find('/news/20') != -1:
                all_urls.append(default_url + link['href'])
                load_page(default_url + link['href'], len(all_urls))
                print("COUNT OF URLS:  " + str(len(all_urls)))


def save_pages(max_count):
    for url in base_urls:
        if len(all_urls) >= max_count:
            return 0
        else:
            tmp_page = urlopen(url)
            tmp_html_bytes = tmp_page.read()
            tmp_html = tmp_html_bytes.decode("utf-8")
            get_urls_from_page(tmp_html)


save_pages(count)