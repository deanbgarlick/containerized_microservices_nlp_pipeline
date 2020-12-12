import spacy


class NerModel:

    _instance = None
    _model = spacy.load("en_core_web_sm")

    def __init__(self):
        raise Exception('Call instance()')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def transform(self, text):
        doc = self._model(text)
        organizations = set([ent.text.title() for ent in doc.ents if ent.label_ == 'ORG'])
        persons = set([ent.text.title() for ent in doc.ents if ent.label_ == 'PERSON'])
        return {'persons': list(persons), 'organizations': list(organizations)}

    def batch_transform(self, X):
        X = pd.DataFrame({'text': X})
        return X['text'].apply(self.transform)


if __name__ == '__main__':

    import pandas as pd

    email_data_df = pd.read_csv('./data/emails_cleaned.csv', nrows=100)
    model = NerModel.instance()
    print(model.batch_transform(email_data_df['body'].astype(str)))
