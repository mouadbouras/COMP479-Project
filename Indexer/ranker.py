import json
import sys
import operator

from afinn import Afinn

from Indexer import Indexer
from Indexer import Tokenizer
from Indexer import Tools

from collections import OrderedDict
from operator import itemgetter



class Ranker(object):

    # calls function to rank results by sentiment
    # limits number of results to amount passed in topx 
    def do_ranking(query, result, files, topx):
        rankedresults = Ranker.rank_by_sentiment(query, result, files)
        # itemcnt = 0
        # print(rankedresults)
        # for k in rankedresults:
        #     if itemcnt >= topx:
        #         rankedresults.pop(k)
        #     itemcnt += 1
        return rankedresults[:topx]

    def open_json(index_file):
        data = Tools.loadDictionary(index_file)
        return data

    # rank by sentiment taking query, dict{docId, tf-idf}, files
    # if sentiment(query) >= 0 : rank docs from positive to negative
    # else : rank docs from negative to positive
    def rank_by_sentiment_OLD(query, docweights, files):
        querysentiment = Tools.sentiment(query)
        docsentiments = {}
        ordereddocs = OrderedDict()
        for k in docweights.keys():
            doc = Tools.getDocById(k, files)
            docsentiments[k] = Tools.sentiment(doc)
        if querysentiment >= 0:
            ordereddocs = sorted(docsentiments,  reverse=True)
        else:
            ordereddocs = sorted(docsentiments, )
        return ordereddocs

    def rank_by_sentiment(query, query_result, files):
        print(query_result)
        pos = []
        neg = []
        querysentiment = Tools.sentiment(query)

        for doc in sorted(query_result, key=query_result.get,  reverse=True): 
            document = Tools.getDocById(doc, files)
            docsentiment = Tools.sentiment(document)
            # print(str(doc) + "|" + str(docsentiment))
            if docsentiment >= 0:
                pos.append(doc)
            else :
                neg.append(doc)
        # print(pos)
        # print(neg)
        if querysentiment >= 0:
            pos.extend(neg)
            return pos
        else:
            neg.extend(pos)
            return neg

        
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
        return sortedweights


    #returns dictionary of {term : [doclist]} for each query term 
    def get_query_docs(query, index):
        querytokens = Tokenizer.tokenize(query)
        result = {}
        for word in querytokens:
            # print(word in index)
            if word in index:
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

        RankedKeys =  sorted(final_dict.items(), key=operator.itemgetter(1),reverse=True)

        return [final_dict,RankedKeys]
        




