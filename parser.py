import requests
from bs4 import BeautifulSoup
import requests
import os
import csv


HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
           'accept': '*/*'}
HOST = 'https://www.avito.ru'
FILE = 'jobs.csv'

def get_html(URL, params = None):
    r = requests.get(URL,headers=HEADERS, params=params, timeout=30)
    return r

def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', class_='pagination-root-Ntd_O')
    line = pagination.text
    p_count = int(line[-9:-7])
    if p_count > 1:
        return p_count
    else:
        return 1

def save_file(items, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow(['Специальность', 'Зарплата в рублях', 'Ссылка'])
        for item in items:
             writer.writerow([item['title'], item['rub'], item['link']])

def check_file(path):
    return os.path.exists(path)

def delete_file(path):
    os.remove(path)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='js-catalog-item-enum')
    jobs = []
    for item in items:
        jobs.append({
            'title' : item.find('h3', class_='text-bold-SinUO').get_text(),
            'rub' : item.find('span', class_='text-size-s-BxGpL').get_text().replace('\xa0', ' ').replace('₽', ''),
            'link' : HOST + item.find('a', class_='title-root_maxHeight-SXHes').get('href')
        })
    return jobs

def parse():
    URL = input('Введите нужную ссылку на Авито: ')
    URL.split()
    html = get_html(URL)
    if html.status_code == 200:
        jobs = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count+1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            jobs.extend(get_content(html.text))
        print(f'Найдено {len(jobs)} предложений по работе')
        file_exists = check_file(FILE)
        if file_exists:
            delete_file(FILE)
            save_file(jobs, FILE)
            os.startfile(FILE)
        else:
            save_file(jobs, FILE)
            os.startfile(FILE)
    else:
        print(html.status_code)
        print('Error')
    
parse() 