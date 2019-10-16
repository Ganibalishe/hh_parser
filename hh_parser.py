import time
import csv
import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
           }

base_url = 'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_period=3&text=python&page=0'


def hh_parse(base_url, headers):
    jobs = []
    urls = []
    urls.append(base_url)
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        start = time.time()
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&search_period=3&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass
    for url in urls:
        request = session.get(url, headers=headers)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                description = text1 + ' ' + text2
                jobs.append({
                    'title': title,
                    'company': company,
                    'href': href,
                    'description': description
                })
            except:
                pass
        print(len(jobs))
        finish = time.time() - start
    else:
        print('Status code = ' + str(request.status_code))
    print('lxml = ' + str(finish))
    return jobs


def files_writer(jobs):
    with open('parsed_jobs.csv', 'w') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('Название Вакансии', 'URL', 'Название компании', 'Описание'))
        for job in jobs:
            a_pen.writerow((job['title'], job['href'], job['company'], job['description']))


jobs = hh_parse(base_url, headers)
files_writer(jobs)

