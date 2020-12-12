import email
import os
from flask import request, jsonify, Flask
import requests


app = Flask(__name__)


@app.route("/")
def index():

    app_name = os.getenv("APP_NAME")

    if app_name:
        return f"Hello from {app_name} running in a Docker container behind Nginx!"

    return "Hello from Flask"


@app.route("/email", methods = ['POST'])
def process_email():

    email_string = request.json['email_string']
    parsed_email = email.parser.Parser().parsestr(email_string)

    check_company_res = requests.post('http://check_company_microservice:8080/email', json={"email_string": email_string})
    sentiment_res = requests.post('http://sentiment_microservice:5000/text', json={"text": parsed_email._payload}, timeout=3000)


    if check_company_res.json()['email_contains_enron']:
        label_topic_res = requests.post('http://label_topic_microservice:8080/text', json={"text": parsed_email._payload})
        topic_label = label_topic_res.json()['topic_label']

        if label_topic_res.json()['topic_label'] == 'oil and gas':
            ner_res = requests.post('http://ner_microservice:8080/text', json={"text": parsed_email._payload})
            relevant_persons = ner_res.json()['persons']
            relevant_organizations = ner_res.json()['organizations']
        else:
            relevant_persons = []
            relevant_organizations = []

    else:
        topic_label = ''
        relevant_persons = []
        relevant_organizations = []

    return jsonify({
        'sentiment_score': sentiment_res.json()['sentiment_score'],
        'email_contains_enron': check_company_res.json()['email_contains_enron'],
        'topic_label': topic_label,
        'relevant_persons': relevant_persons,
        'relevant_organizations': relevant_organizations
    })


if __name__ == '__main__':

    import requests
    import pandas as pd

    emails_df = pd.read_csv('data/emails.csv')
    for i in range(emails_df.shape[0]):
        message_string = emails_df.iloc[i].message
        res = requests.post('http://localhost:8080', json={"text": message_string})
        print(res.json())