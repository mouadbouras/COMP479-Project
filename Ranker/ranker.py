import json
import sys

import ntlk
from afinn import Afinn

from ..Tokenizer import Tokenizer


class Ranker(object):

    def open_json(index):
        data = json.load(open(index))

    def rank_document(document):
        afinn = Afinn()
        tokens = Tokenizer.tokenize(document)
        sentiment = 0
        for token in tokens :
            sentiment += afinn.score(token)
        return sentiment

    def query_sentiment(query):
        afinn = Afinn()
        querytokens = Tokenizer.tokenize(query)
        sentiment = 0
        for token in querytokens :
            sentiment += afinn.score(token)
        return sentiment
