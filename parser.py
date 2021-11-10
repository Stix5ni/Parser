import requests
from bs4 import BeautifulSoup

import os

import csv

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
           'accept': '*/*'}
HOST = 'https://www.avito.ru'
FILE = 'jobs.csv'
my_dir = 'C:/Users/Happy/Desktop/All about python//DB'
FNAME = os.path.join(my_dir, FILE) #полный путь сохраняемого файла


class WorkWithFile():
    '''Работа системы с файлами'''
    def __init__(self):
        pass
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
        
def get_html(URL, params = None): #получение html-страницы
    r = requests.get(URL,headers=HEADERS, params=params, timeout=30)
    return r

def get_pages_count(html): #получение кол-ва страниц
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('div', class_='pagination-root-Ntd_O'): #проверка на нахождение кол-ва страниц
        pagination = soup.find('div', class_='pagination-root-Ntd_O')
        line = pagination.text
        p_count = int(line[-9:-7])
        if p_count > 1:
            return p_count
        else:
            return 1
    else:
        return 1

def get_content(html): #получение определённого контента от html-страницы
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

def get_parsing_result(pages_count, URL, jobs): #прогон парсинга
    for page in range(1, pages_count+1):
        print(f'Парсинг страницы {page} из {pages_count}...')
        html = get_html(URL, params={'page': page})
        jobs.extend(get_content(html.text))
    return jobs

def parse(): #парсинг страницы
    URL = input('Введите нужную ссылку на Авито: ')
    URL.split()
    html = get_html(URL)
    if html.status_code == 200:
        jobs = []
        pages_count = get_pages_count(html.text)
        get_parsing_result(pages_count, URL, jobs)
        print(f'Найдено {len(jobs)} предложений по работе')
        file_exists = WorkWithFile.check_file(FNAME)
        if file_exists:
            WorkWithFile.delete_file(FNAME)
            WorkWithFile.save_file(jobs, FNAME)
            os.startfile(FNAME)
        else:
            WorkWithFile.save_file(jobs, FNAME)
            os.startfile(FNAME)
    else:
        print(html.status_code)
        print('Error')
    
parse() 