import os
import time
from flask import request, jsonify, Flask
from transformer import MultilingualUncasedSentimentTransformer


app = Flask(__name__)
MultilingualUncasedSentimentTransformer.instance()


@app.route("/text", methods = ['POST'])
def main():
    text = request.json['text']
    print('in sentiment microservice')
    start_time = time.time()
    transformer = MultilingualUncasedSentimentTransformer.instance()
    print('obtained transformer:')
    print(time.time() - start_time)
    sentiment_score = transformer.transform(text)
    print('obtained sentiment score')
    print(time.time() - start_time)
    return jsonify({'sentiment_score': sentiment_score})


if __name__ == '__main__':

    import email
    import pandas as pd

    emails = pd.read_csv('data/emails.csv', nrows=10)
    email_ner_list = []
    model = MultilingualUncasedSentimentTransformer.instance()

    for i in range(0, 10):
        email_ = emails.iloc[i]['message']
        email_parsed = email.parser.Parser().parsestr(email_)
        email_ner_list.append(model.transform(email_parsed._payload))

    print(email_ner_list)