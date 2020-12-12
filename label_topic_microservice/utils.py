import re
import spacy


class EmailCleaningService:

    _instance = None
    _model = spacy.load("en_core_web_sm")
    _lines_to_remove = (
        'returnpath:',
        'xoriginatingip:',
        'subject:',
        'sent:',
        'from:',
        'to:',
        'returnpath:',
        'date:',
        'xoriginalarrivaltime:',
        'cc:',
        'forwardedby',
        'originalmessage',
        'file:',
        'contentdisposition:',
        'contenttype:',
        'messageid:',
        'xmimetrack:',
        'contenttransferencoding:',
        'received:',
        'boundary=',
        'name=',
        'seeattachedfile:',
        'mimeversion:'
    )

    def __init__(self):
        raise Exception('Call instance()')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def __call__(self, text):
        text = self.remove_long_words(text)
        text = self.remove_email_header_lines(text)
        text = self.remove_digital_addresses_from_text(text)
        text = self.remove_names_and_dates_from_text(text)
        text = self.remove_numbers(text)
        text = text.replace('\n', ' ')
        text = self.remove_punctuation(text)
        return text

    def remove_names_and_dates_from_text(self, text):
        doc = self._model(text)
        for ent in doc.ents:
            if ent.label_ == 'PERSON' or ent.label_ == 'DATE':
                text = text.replace(ent.text, '')
        return text

    def remove_email_header_lines(self, email_text):
        lines = email_text.split('\n')
        for n, line in enumerate(lines):
            no_punctuation_line = re.sub('[!"#$%&\'()*+,-./;<>?@[\\]^_`{|}~]', "", line) # remove punctuation except colons
            no_spaces_line = no_punctuation_line.replace(' ', '')
            if no_spaces_line.lower().startswith(self._lines_to_remove):
                lines[n] = '\n'
        return '\n'.join(lines)

    @staticmethod
    def remove_punctuation(text):
        return re.sub('[!"#$%&\'()*+:,-./;<>?@[\\]^_`{|}~]', "", text)

    @staticmethod
    def remove_numbers(text):
        return re.sub('[0123456789]', "", text)

    @staticmethod
    def replace_digital_addresses_in_text(email_text):
        tokens = email_text.split(' ')
        for n, token in enumerate(tokens):
            if ('@' in token) and ('.com' in token):
                tokens[n] = 'emailaddress'
        for n, token in enumerate(tokens):
            if '.com' in token:
                tokens[n] = 'webaddress'
        text = ' '.join(tokens)
        return text

    @staticmethod
    def remove_digital_addresses_from_text(text):
        text = text.replace('emailaddress', '')
        text = text.replace('webaddress', '')
        return text

    @staticmethod
    def remove_long_words(text):
        tokens_list = text.split(' ')
        tokens_list = list(filter(lambda x: len(x) < 45, tokens_list))
        text = ' '.join(tokens_list)
        return text
