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
        return data
        
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


    #returns dictionary of {term : [doclist]} for each query term 
    def get_query_docs(query, index):
        querytokens = Tokenizer.tokenize(query)
        result = {}
        for word in querytokens:
            result[word] = index[word][0]
        return result

    #takes the dictionary of {term : [doclist]} then for each docID of each query it calculates the Tf-Idf
    def rank_results(query_result, index, files, topx):
        ranking = {}
        for term in query_result :
            ranking[term] = []
            for doc in query_result[term] :
                # print(doc)
                tmp = [] 
                tmp.append(doc)
                tmp.append(Tools.tf_idf(term,doc,index , files ))
                ranking[term].append(tmp)
                # print(ranking)
        return ranking 
    







