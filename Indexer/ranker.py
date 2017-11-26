import json
import sys
# sys.path.append('..')
import operator

import nltk
from afinn import Afinn

from Indexer import Indexer
from Indexer import Tokenizer
from Indexer import Tools

from collections import OrderedDict
from operator import itemgetter


class Ranker(object):

    def open_json(index_file):
        data = Tools.loadDictionary(index_file)
        return data

    # rank by sentiment
    # if sentiment(query) >= 0 : rank docs from positive to negative
    # else : rank docs from negative to positive
    def rank_by_sentiment(query, docweights, files):
        querysentiment = Tools.sentiment(query)
        docsentiments = {}
        ordereddocs = OrderedDict()
        for k in docweights.keys():
            doc = Tools.getDocById(k, files)
            docsentiments[k] = Tools.sentiment(doc)
        if querysentiment >= 0:
            ordereddocs = sorted(docsentiments, key=itemgetter(1), reverse=True)
        else:
            ordereddocs = sorted(docsentiments, key=itemgetter(1))
        return ordereddocs
        
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
    def rank_results(query_result, index, files):
        ranking = []
        # ranking = {} --> per term
        for term in query_result :
            # ranking ranking[term] = []--> per term
            for doc in query_result[term] :
                # print(doc)
                tmp = [] 
                tmp.append(doc)
                tmp.append(Tools.tf_idf(term,doc,index , files ))
                # ranking[term].append(tmp)--> per term
                ranking.append(tmp)
                

        return ranking 
    
    #this function executes the query and returns an UNORDERD dictionary {docid : grade, docid : grade, docid : grade } 
    # as well as an ORDERED list of tuples [(docid,grade),(docid,grade),(docid,grade)] ASCENDING

    def exec_query(query,index,files):
        query_result = Ranker.get_query_docs(query, index)
        ranked_results = Ranker.rank_results(query_result, index, files )
        final_dict = {}
        for result in ranked_results :
            if result[0] in final_dict:
                if final_dict[result[0]] < result[1] : 
                    final_dict[result[0]] = result[1]
            else : 
                final_dict[result[0]]=result[1]

        RankedKeys =  sorted(final_dict.items(), key=operator.itemgetter(1))

        return [final_dict,RankedKeys]
        




