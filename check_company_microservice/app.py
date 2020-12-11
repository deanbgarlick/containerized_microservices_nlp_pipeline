import email
from flask import request, jsonify
import os
import pandas as pd

from flask import Flask

app = Flask(__name__)


def text_contains_enron(text_body):
    lowercase_text_body = str(text_body).lower()
    return 'enron' in lowercase_text_body


def email_contains_enron(email_record):
    bool_ = True in email_record.apply(text_contains_enron).values
    return bool_


def emails_in_batch_contain_enron(email_df):
    return email_df.apply(email_contains_enron, axis=1)


@app.route("/email", methods = ['POST'])
def main():
    email_string = request.json['email_string']
    parsed_email = email.parser.Parser().parsestr(email_string)
    email_batch = pd.DataFrame.from_records([parsed_email.__dict__])
    enron_related = True in emails_in_batch_contain_enron(email_batch)
    return jsonify({'email_contains_enron': enron_related})


if __name__ == '__main__':

    emails = pd.read_csv('data/emails.csv', nrows=10)

    email_records = []

    for i in range(0, 10):
        email_ = emails.iloc[i]['message']
        email_parsed = email.parser.Parser().parsestr(email_)
        email_records.append(email_parsed.__dict__)

    email_batch = pd.DataFrame(email_records)
    print(emails_in_batch_contain_enron(email_batch))
