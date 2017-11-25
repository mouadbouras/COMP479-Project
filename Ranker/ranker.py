import json
import sys
sys.path.append('..')

import nltk
from afinn import Afinn

from Indexer import Indexer
from Indexer import Tokenizer
from Indexer import Tools


class Ranker(object):

    def open_json(index):
        data = json.load(open(index))

    def rank_document(document):
        afinn = Afinn()
        tokens = Tokenizer.tokenize(document)
        sentiment = 0
        for token in tokens:
            sentiment += afinn.score(token)
        return sentiment

    def query_sentiment(query):
        afinn = Afinn()
        querytokens = Tokenizer.tokenize(query)
        sentiment = 0
        for token in querytokens:
            sentiment += afinn.score(token)
        return sentiment
