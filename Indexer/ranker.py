import json
import sys
# sys.path.append('..')

import nltk
from afinn import Afinn

from Indexer import Indexer
from Indexer import Tokenizer
from Indexer import Tools

from collections import OrderedDict


class Ranker(object):

    def open_json(index_file):
        data = Tools.loadDictionary(index_file)
        
    # docs = only docs returned by query result, not everything in the index
    # recalculates tf for every doc, not sure whether to adjust
    def rank_docs_tfidf(query, index, docs, files, topx):
        termweights = {}
        querytokens = Tokenizer.tokenize(query)
        for doc in docs:
            docId = Tools.getDocId(doc)
            for term in querytokens:
                termweights[term] = Tools.tf_idf(term, docId, index, files)
        sortedweights = OrderedDict(sorted(termweights.values))
        itemcnt = 0
        for k, v in sortedweights.items():
            if itemcnt >= topx:
                sortedweights.pop(k)
            itemcnt += 1
        return sortedweights

    # can use Tools.sentiment(query) instead
    def query_sentiment(query):
        afinn = Afinn()
        querytokens = Tokenizer.tokenize(query)
        sentiment = 0
        for token in querytokens:
            sentiment += afinn.score(token)
        return sentiment
