import requests
import datetime
def check_name(vac_name):
    available_names = ('баз данных', 'оператор баз данных', 'базы данных', 'oracle', 'mysql', 'data base', 'database', 'dba', 'bd', 'бд', 'базами данны')
    for available_name in available_names:
        if available_name in vac_name:
            return True

def search():
    url = 'https://api.hh.ru/vacancies'
    date_to = datetime.datetime.now()
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)

    page_number = 0
    iso_date_to = datetime.datetime.isoformat(date_to)
    iso_date_from = datetime.datetime.isoformat(date_from)

    found_vacancies = []

    while len(found_vacancies) == 0:
        
        answer = requests.get(url, params={'page':page_number, 'date_from':iso_date_from, 'date_to':iso_date_to})
        json_format = answer.json()
        vacancies = json_format['items']
        for vacancy in vacancies:
            vacancy_url = vacancy['url']
            vac_name = vacancy['name']
            if check_name(vac_name):
                
                #print(vacancy['name'])
                if len(found_vacancies)<10:
                    found_vacancies.append(vacancy)
                else:
                    return found_vacancies
        if len(found_vacancies) == 0:
            page_number +=1
            if page_number == json_format['pages']:
                #print('не нашел')
                #print('сдвигаю даты')
                date_from = date_from - datetime.timedelta(days=1)
                date_to = date_to - datetime.timedelta(days=1)
                iso_date_from = datetime.datetime.isoformat(date_from)
                iso_date_to = datetime.datetime.isoformat(date_to)
                page_number = 0
                #print(f'new dates: {date_from} --- {date_to}')

    return found_vacancies