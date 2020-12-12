import os
import json
import pickle
import numpy as np
import pandas as pd
from corextopic import corextopic as ct
from utils import EmailCleaningService
from sklearn.feature_extraction.text import TfidfVectorizer


class CorExTopicModel:

    _instance = None

    def __init__(self):

        self._vectorizer = None
        self._model = None
        self._topic_hash = None
        self._oil_and_gas_topic_num = None

    def to_disk(self):
        os.makedirs('model', exist_ok=True)
        with open('model/topic_hash.json', 'w') as f:
            json.dump(self._topic_hash, f)
        with open('model/vectorizer.pkl', 'wb') as f:
            pickle.dump(self._vectorizer, f)
        with open('model/model.pkl', 'wb') as f:
            pickle.dump(self._model, f)

    @classmethod
    def from_disk(cls):
        self = cls.__new__(cls)
        with open('model/topic_hash.json', 'r') as f:
            self._topic_hash = json.load(f)
        with open('model/vectorizer.pkl', 'rb') as f:
            self._vectorizer = pickle.load(f)
        with open('model/model.pkl', 'rb') as f:
            self._model = pickle.load(f)
        self._oil_and_gas_topic_num = [int(topic_num) for topic_num, topic_ngrams in self._topic_hash.items() if ('oil' in topic_ngrams) or ('gas' in topic_ngrams)]
        return self

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.from_disk()
        return cls._instance

    def train(self, df, n_hidden=8, anchors=[["oil", "gas"]], anchor_strength=3):
        print('anchor_strength ', str(anchor_strength), '   n_hidden ', str(n_hidden))
        vectorizer = TfidfVectorizer(
            max_df=.5,
            min_df=10,
            max_features=None,
            ngram_range=(1, 2),
            norm=None,
            binary=True,
            use_idf=False,
            sublinear_tf=False,
            stop_words='english'
        )
        vectorizer = vectorizer.fit(df['body'])
        tfidf = vectorizer.transform(df['body'])
        vocab = vectorizer.get_feature_names()

        # Anchors designed to nudge the model towards measuring specific genres

        anchors = [
            [a for a in topic if a in vocab]
            for topic in anchors
        ]

        model = ct.Corex(n_hidden=n_hidden, seed=42)
        model = model.fit(
            tfidf,
            words=vocab,
            anchors=anchors, # Pass the anchors in here
            anchor_strength=anchor_strength # Tell the model how much it should rely on the anchors
        )

        topic_hash = {}
        for i, topic_ngrams in enumerate(model.get_topics(n_words=10)):
            topic_ngrams = [ngram[0] for ngram in topic_ngrams if ngram[1] > 0]
            topic_hash[i] = topic_ngrams

        self._vectorizer = vectorizer
        self._model = model
        self._topic_hash = topic_hash
        self._oil_and_gas_topic_num = [topic_num for topic_num, topic_ngrams in self._topic_hash.items() if ('oil' in topic_ngrams) or ('gas' in topic_ngrams)]

    def batch_transform(self, X):
        tfidf = self._vectorizer.transform(X)
        topic_array = self._model.transform(tfidf)
        return topic_array

    def transform(self, text):
        text_array = np.array([text])
        topic_array = self.batch_transform(text_array)
        print(topic_array)
        print(self._oil_and_gas_topic_num)
        is_oil_and_gas = np.sum(topic_array[0, self._oil_and_gas_topic_num])
        if is_oil_and_gas:
            topic_estimation = 'oil and gas'
        else:
            topic_estimation = 'not oil or gas'
        return topic_estimation


if __name__ == '__main__':

    import pandas as pd

    email_data_df = pd.read_csv('./data/emails_cleaned.csv', nrows=100)
    email_data_df['text'] = email_data_df['body'].astype(str).apply(EmailCleaningService.instance())
    model = CorExTopicModel.instance()
    print(model.batch_transform(email_data_df['text'].values))
