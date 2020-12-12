import requests
import unittest
import numpy as np
import pandas as pd


class TestGateway(unittest.TestCase):

    def setUp(self):
        self.emails_df = pd.read_csv('data/emails.csv')
        email_string_list = []
        for i in range(self.emails_df.shape[0]):
                email_string_list.append(self.emails_df.iloc[i].message)
        self.email_string_list = email_string_list

    def test_service_response_status_codes(self):
        for email_string in self.email_string_list:
            res = requests.post('http://localhost:80/email', json={"email_string": email_string})
            assert(res.status_code == 200)

    def test_service_capable_of_returning_different_topics(self):
        topic_labels = []
        for email_string in self.email_string_list:
            res = requests.post('http://localhost:80/email', json={"email_string": email_string})
            topic_labels.append(res.json()['topic_label'])
        assert(len(set(topic_labels))!=1)

    def test_service_capable_of_returning_organisations_and_people(self):
        organisations_list = []
        persons_list = []
        for email_string in self.email_string_list:
            res = requests.post('http://localhost:80/email', json={"email_string": email_string})
            organisations_list.append(res.json()['relevant_organizations'])
            persons_list.append(res.json()['relevant_persons'])
        assert(len(organisations_list)!=0)
        assert(len(persons_list)!=0)

    def test_people_and_organisations_only_returned_when_topic_is_oil_and_gas(self):
        for email_string in self.email_string_list:
            res = requests.post('http://localhost:80/email', json={"email_string": email_string})
            if res.json()['topic_label'] == 'not oil and gas':
                assert(len(res.json()['relevant_organizations'])==0)
                assert(len(res.json()['relevant_persons'])==0)


if __name__ == '__main__':
    unittest.main()