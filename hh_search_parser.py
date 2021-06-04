import requests
import json
import time
import os
from tqdm import tqdm


class HHSearchParser:
    def __init__(self, search_line,  amount_of_pages = 1):
        self.search_line = search_line
        self.amount_of_pages = amount_of_pages

    def get_vacancy(self, page_num):
        params = {
            'text': self.search_line,
            'page': page_num,
            'items_on_page': 100,
            'order_by': 'relevance',
            'area': 113  #Россия
        }
        req = requests.get('https://api.hh.ru/vacancies', params)
        data = req.content.decode()
        req.close()
        return data

    def create_search_files(self):
        for file in os.listdir('./search_docs'):
            os.remove('./search_docs/' + file)
        print('Началась закачка результатов поиска вакансий')
        for p in tqdm(range(0, self.amount_of_pages+1)):
            js = json.loads(self.get_vacancy(p))
            next_file_name = './search_docs/{}.json'.format(len(os.listdir('./search_docs')))
            f = open(next_file_name, mode='w', encoding='utf8')
            f.write(json.dumps(js, ensure_ascii=False))
            f.close()
            if (js['pages'] - p) <= 1:
                break
            time.sleep(0.25)




