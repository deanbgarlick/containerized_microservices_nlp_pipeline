import os
from flask import request, jsonify, Flask
from transformer import CorExTopicModel


app = Flask(__name__)
CorExTopicModel.instance()


@app.route("/text", methods = ['POST'])
def main():
    text = request.json['text']
    transformer = CorExTopicModel.instance()
    topic_label = transformer.transform(text)
    return jsonify({'topic_label': topic_label})


if __name__ == '__main__':

    import email
    import pandas as pd

    emails = pd.read_csv('data/emails.csv', nrows=10)
    email_ner_list = []
    model = CorExTopicModel.instance()

    for i in range(0, 10):
        email_ = emails.iloc[i]['message']
        email_parsed = email.parser.Parser().parsestr(email_)
        email_ner_list.append(model.transform(email_parsed._payload))

    print(email_ner_list)