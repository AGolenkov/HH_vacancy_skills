import pandas as pd
import json
import os
from IPython import display
import regex as re

# таблица описаний вакансий
vac_id = []
vac_name = []
vac_description = []
vac_employer = []

# таблица навыков и вакансий
vac_skill_id = []
vac_skill_name = []

cnt_vac = len(os.listdir('./vacancies'))
i = 0

for vac in os.listdir('./vacancies'):

    f = open('./vacancies/{}'.format(vac), encoding='utf8')
    vac_json_text = f.read()
    f.close()

    # Текст файла переводим в справочник
    vac_json_object = json.loads(vac_json_text)

    # Заполняем списки для таблицы описаний вакансий
    vac_id.append(vac_json_object['id'])
    vac_name.append(vac_json_object['name'])
    vac_description.append(re.sub('<[^<]+?>', '', vac_json_object['description']))
    vac_employer.append(vac_json_object['employer']['name'])

    # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
    for skl in vac_json_object['key_skills']:
        vac_skill_id.append(vac_json_object['id'])
        vac_skill_name.append(skl['name'])

    # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
    i += 1
    display.clear_output(wait=True)
    display.display('Готово {} из {}'.format(i, cnt_vac))

df_vac = pd.DataFrame({'vacancy_id': vac_id, 'vacancy_name': vac_name, 'vacancy_desc': vac_description, 'vac_employer': vac_employer})
df_vac.to_excel('./data/vac_info.xlsx')

df_vac_skills = pd.DataFrame({'vacancy_id': vac_skill_id, 'skill_name': vac_skill_name})
df_vac_skills.to_excel('./data/vac_skills.xlsx')

