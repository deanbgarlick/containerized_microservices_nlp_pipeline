import numpy as np
import pandas as pd
import scipy.special
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class MultilingualUncasedSentimentTransformer():

    _instance = None

    tokenizer = AutoTokenizer.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    model = AutoModelForSequenceClassification.from_pretrained("nlptown/bert-base-multilingual-uncased-sentiment")
    padding = False
    truncation = 'longest_first'
    return_tensors = "pt"

    def __init__(self):
        raise Exception('Call instance()')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def fit(self, X, y=None):
        return self

    def transform(self, email_body):
        with torch.no_grad():
            tokens = self.tokenizer([str(email_body)], truncation=self.truncation, return_tensors=self.return_tensors)['input_ids']
            logits = self.model(tokens)['logits'].numpy()
            sentiment_score_probabilities = scipy.special.softmax(logits)
            sentiment_score_probabilities = np.squeeze(sentiment_score_probabilities)
            expected_value_sentiment_score = np.sum(np.multiply(sentiment_score_probabilities, np.array([1.,2.,3.,4.,5.])))
            return expected_value_sentiment_score

    def batch_transform(self, X):
        X = pd.DataFrame({'text': X})
        return X['text'].apply(self.transform)


if __name__ == '__main__':

    email_data_df = pd.read_csv('./data/emails_cleaned.csv', nrows=10)
    must = MultilingualUncasedSentimentTransformer.instance()
    print(must.batch_transform(email_data_df['body'].astype(str)))
