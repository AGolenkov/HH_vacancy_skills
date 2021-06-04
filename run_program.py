import hh_search_parser
import hh_vacancy_parser
import create_vac_data
import vacancy_classifier
import vacancy_topic_extractor
import subprocess
import os


search_line = input('Введите поисковый запрос: ')
amount_of_pages = input('Укажите количество страниц, считываемых с сайта HH.ru: ')
n_clust = input('Введите число кластеров для вакансий: ')
n_topics = input('Введите число выделяемых топиков: ')
hh_search = hh_search_parser.HHSearchParser(search_line = search_line,  amount_of_pages = int(amount_of_pages))
hh_search.create_search_files()
hh_vacancy_parser.hh_vacancy_parser()
create_vac_data.export_vacancy_main_data()
vac_classifier = vacancy_classifier.VacancyClassifier(n_clust=int(n_clust))
vac_classifier.classificator()
topic_extractor = vacancy_topic_extractor.TopicExtractor(n_topics=int(n_topics))
topic_extractor.get_topics()
print()
print('Данные для дашборда успешно сформированы')
subprocess.run(['explorer', os.path.realpath('./data')])
