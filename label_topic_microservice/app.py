import os
from flask import request, jsonify, Flask
from transformer import CorExTopicModel
from utils import EmailCleaningService


app = Flask(__name__)
EmailCleaningService.instance()
CorExTopicModel.instance()


@app.route("/text", methods = ['POST'])
def main():
    text = request.json['text']
    text = EmailCleaningService.instance()(text)
    print(text)
    transformer = CorExTopicModel.instance()
    topic_label = transformer.transform(text)

    return jsonify({'topic_label': topic_label})


if __name__ == '__main__':

    import email
    import pandas as pd

    emails = pd.read_csv('data/emails.csv', nrows=10)
    model = CorExTopicModel.instance()
    email_topic_list = []

    for i in range(0, 10):
        email_ = emails.iloc[i]['message']
        email_parsed = email.parser.Parser().parsestr(email_)
        text = EmailCleaningService.instance()(email_parsed._payload)
        topic_prediction = model.transform(text)
        email_topic_list.append(topic_prediction)

    print(email_topic_list)