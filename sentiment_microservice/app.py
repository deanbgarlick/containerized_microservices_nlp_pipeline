import os
import time
from flask import request, jsonify, Flask
from transformer import MultilingualUncasedSentimentTransformer
from utils import take_top_email_from_chain

app = Flask(__name__)
MultilingualUncasedSentimentTransformer.instance()


@app.route("/text", methods = ['POST'])
def main():
    email_chain_text = request.json['text']
    top_email_text = take_top_email_from_chain(email_chain_text)
    transformer = MultilingualUncasedSentimentTransformer.instance()
    sentiment_score = transformer.transform(top_email_text)
    return jsonify({'sentiment_score': sentiment_score})


if __name__ == '__main__':

    import email
    import pandas as pd

    emails = pd.read_csv('data/emails.csv', nrows=10)
    email_sentiment_list = []
    model = MultilingualUncasedSentimentTransformer.instance()

    for i in range(0, 10):
        email_ = emails.iloc[i]['message']
        email_parsed = email.parser.Parser().parsestr(email_)
        email_text = email_parsed._payload
        top_email_text = take_top_email_from_chain(email_text)
        email_sentiment_list.append(model.transform(top_email_text))

    print(email_sentiment_list)