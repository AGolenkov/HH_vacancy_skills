import json
import os
import requests
import time
from tqdm import tqdm


def hh_vacancy_parser():
    for file in os.listdir('./vacancies'):
        os.remove('./vacancies/' + file)
    time.sleep(2)
    print('Началось формирование вакансий из результатов поиска')
    for file_num in tqdm(os.listdir('./search_docs')):
        f = open('./search_docs/{}'.format(file_num), encoding='utf8')
        vac_json_text = f.read()
        f.close()
        vac_json_object = json.loads(vac_json_text)

        for vacancy in vac_json_object['items']:
            req = requests.get(vacancy['url'])
            vac_data = req.content.decode()
            req.close()
            file_name = './vacancies/{}.json'.format(vacancy['id'])
            vac_f = open(file_name, mode='w', encoding='utf8')
            vac_f.write(vac_data)
            vac_f.close()
            time.sleep(0.25)