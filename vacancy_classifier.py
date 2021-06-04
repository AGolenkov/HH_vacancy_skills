import pandas as pd
from pymorphy2 import MorphAnalyzer
from stop_words import get_stop_words
from string import punctuation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import cluster


class VacancyClassifier:
    def __init__(self, n_clust=5):
        self.df_vac_name = pd.read_excel('./data/vac_info.xlsx')
        self.df_vac_name = self.df_vac_name[['vacancy_id', 'vacancy_name']]
        self.df_vac_name = self.df_vac_name.set_index('vacancy_id')
        self.exclude_punctuation = set(punctuation)
        self.stop_words = set(get_stop_words("ru"))
        self.morpher = MorphAnalyzer()
        self.n_clust = n_clust

    def preprocess_text(self, txt):
        txt = str(txt)
        txt = "".join(c for c in txt if c not in self.exclude_punctuation)
        txt = txt.lower()
        txt = [self.morpher.parse(word)[0].normal_form for word in txt.split() if word not in self.stop_words]
        return " ".join(txt)

    def classificator(self):
        self.df_vac_name['vacancy_name'] = self.df_vac_name['vacancy_name'].apply(self.preprocess_text)
        tfidf = TfidfVectorizer()
        corpus = tfidf.fit_transform(self.df_vac_name['vacancy_name'])
        model = cluster.KMeans(n_clusters=self.n_clust)
        res = model.fit_predict(corpus)
        self.df_vac_name['cluster'] = res
        self.df_vac_name.to_excel('./data/vac_clustered.xlsx')
        print('Вакансии успешно кластеризованы')
