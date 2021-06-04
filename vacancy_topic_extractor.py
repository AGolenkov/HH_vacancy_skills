import pandas as pd
from pymorphy2 import MorphAnalyzer
from stop_words import get_stop_words
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from tqdm import tqdm
import time


class TopicExtractor:
    def __init__(self, n_topics = 20):
        self.df_vac_desc = pd.read_excel('./data/vac_info.xlsx')
        self.df_vac_desc = self.df_vac_desc[['vacancy_id', 'vacancy_desc']]
        self.exclude_punctuation = set(punctuation)
        self.stop_words = set(get_stop_words("ru"))
        with open('additional_stop_words.txt', 'r', encoding='utf8') as f:
            stop_words_txt = f.read()
        stop_words_txt = stop_words_txt.replace('\n', '')
        stop_words_txt = stop_words_txt.replace(' ', '')
        self.stop_work_words = set(stop_words_txt.split(','))
        self.stop_words.update(self.stop_work_words)
        self.morpher = MorphAnalyzer()
        self.n_topics = n_topics

    def preprocess_text(self, txt):
        txt = str(txt)
        txt = "".join(c for c in txt if c not in self.exclude_punctuation)
        txt = txt.lower()
        txt = [self.morpher.parse(word)[0].normal_form for word in txt.split() if word not in self.stop_words]
        txt = [word for word in txt if word not in self.stop_words]
        return " ".join(txt)

    def get_topics(self):
        print('Началось преобразование текстов для извлечения топиков')
        self.df_vac_desc['vacancy_desc'] = self.df_vac_desc['vacancy_desc'].apply(self.preprocess_text)
        print('Началось извлечение топиков ...')
        vect = CountVectorizer()
        corpus = vect.fit_transform(self.df_vac_desc['vacancy_desc'])
        model = LatentDirichletAllocation(n_components=self.n_topics)
        model.fit_transform(corpus)
        names = vect.get_feature_names()
        topics = dict()

        for idx, topic in enumerate(model.components_):
            features = topic.argsort()[:-(6 - 1): -1]
            tokens = [names[i] for i in features]
            topics[idx] = tokens
        self.df_vac_desc['word_list'] = self.df_vac_desc['vacancy_desc'].apply(lambda x: x.split())
        sentences = self.df_vac_desc['word_list']
        topic_amount = {key: [] for key in range(self.n_topics)}
        for topic in range(self.n_topics):
            for sentence in sentences:
                amount = 0
                for word in sentence:
                    if word in topics[topic]:
                        amount += 1
                    else:
                        continue
                topic_amount[topic].append(amount)
        topic_df = pd.DataFrame.from_dict(topic_amount)
        topic_df = topic_df.T
        topic_df = topic_df.iloc[lambda x: x.index].apply(lambda x: x / x.sum())
        topic_df = topic_df.T
        topic_df['vacancy_id'] = self.df_vac_desc['vacancy_id']
        topic_df = topic_df.set_index('vacancy_id')
        res_topic = pd.DataFrame(topic_df.stack())
        res_topic.reset_index(inplace=True)
        res_topic = res_topic.rename(columns={'level_1': 'topic_id', 0: 'topic_percent'})
        res_topic.to_excel('./data/vac_topic.xlsx')
        topics_dict = pd.DataFrame.from_dict(topics)
        topics_dict.T.to_excel('./data/topic_dict.xlsx')
        print('Извлечение топиков выполнено успешно')