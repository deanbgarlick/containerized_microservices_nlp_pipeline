from flask import Flask
import os
from flask import request, jsonify
from transformer import NerModel


app = Flask(__name__)
NerModel.instance()


@app.route("/text", methods = ['POST'])
def main():
    text = request.json['text']
    transformer = NerModel.instance()
    persons_and_organizations = transformer.transform(text)
    return jsonify(persons_and_organizations)


if __name__ == '__main__':

    import email
    import pandas as pd

    emails = pd.read_csv('data/emails.csv', nrows=10)
    email_ner_list = []
    model = NerModel.instance()

    for i in range(0, 10):
        email_ = emails.iloc[i]['message']
        email_parsed = email.parser.Parser().parsestr(email_)
        email_ner_list.append(model.transform(email_parsed._payload))

    print(email_ner_list)