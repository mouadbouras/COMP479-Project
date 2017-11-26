import nltk
from afinn import Afinn
import json
import sys
from itertools import chain
from collections import defaultdict
from math import log
from nltk.corpus import stopwords
import codecs, sys, glob, os, unicodedata
import io



from bs4 import BeautifulSoup


class Indexer(object): 

    def index_files(files_list,merge=False):
        fileCounter = 0    
        for file in files_list : 
            dictionary = Indexer.index_file(file)
            Tools.saveObject(dictionary,"Minidict" +str(fileCounter)+ ".json" )
            fileCounter = fileCounter+1
            dictionary = {}
            # print("Postings Count : "+ str(postingCount))
            # print("Term Count : "+ str(dictionaryCount))

        if merge == True : 
            Tools.mergeFiles(fileCounter)    
        return fileCounter

    def index_document(document,docid):
        tokens = Tokenizer.tokenize(document)
        newtokens = []
        for token in tokens :
            newtokens.append([token,docid])
        return newtokens
        
    def index_file(filename):
        tokens = []
        # with open("./" + filename) as fp:
        #     data = fp.read()
        with io.open("../Dumps/" + filename, "r", encoding="utf-8") as fp:
            data = fp.read()        
        # print(data)
        soup = BeautifulSoup(data, "xml")
        documents = soup.find_all("document")
        for document in documents:
            id = int(document["id"])
            body = document.get_text()
            url = document["url"]
            tokens.extend(Indexer.index_document(body,id))          
        
        return Indexer.index(tokens)
            
    def index(tokens):
        afinn = Afinn()
        #print(len(tokens))  
        dictionary= {} 
        postingCount = 0
        dictionaryCount = 0
        for token in tokens :  
            if token[0] not in dictionary : 
                postings_list = []
                # postings_list = {} | USED WITH addToFreqList
                dictionary[token[0]] = []
                dictionary[token[0]].append(postings_list)
                dictionary[token[0]].append(1) 
                dictionary[token[0]].append(afinn.score(token[0]))
                dictionaryCount = dictionaryCount + 1
            else :
                postings_list = dictionary[token[0]][0]
                if (token[1] not in postings_list)  : dictionary[token[0]][1] = dictionary[token[0]][1] + 1
            # length = len(postings_list)
            Indexer.addToList(postings_list,token[1])
            # if(length != len(postings_list)): 
            #     postingCount = postingCount + 1

        return dictionary



    def addToFreqList(postings_list,docid):
        if docid not in postings_list.keys() :
            postings_list[docid] = 1 
        else :
            postings_list[docid] = postings_list[docid] + 1
        return postings_list             

    def addToList(postings_list,docid):
        if docid not in postings_list :
            return postings_list.insert(0,docid) 
        else :
            return postings_list   


class Tokenizer(object): 

    def tokenize(text_document): 

        # remove punctuation
        tbl = dict.fromkeys(i for i in range(sys.maxunicode)
            if unicodedata.category(chr(i)).startswith('P'))        
        text_document = text_document.translate(tbl)    

        # Define stopwords using NLTK standard stopword list for English language
        stopset = set(stopwords.words('english'))
        # Load unicode punctuation

        # print(text_document)
        tokens = nltk.word_tokenize(text_document)
        return tokens 
        

class Tools(object): 

    def saveObject(dictionary,fileName):
        with open(fileName, 'w') as file:
            file.write(json.dumps(dictionary,sort_keys=True))   
        print("File : " + fileName + " saved! ")

    #merge blocks
    def mergeFiles(fileCount):
        with open("../FinalDictionary.json", 'w') as final:         
            final.write("{}")   
        for i in range(0,fileCount):
            print(i)  
            with open("Minidict"+str(i)+".json") as file1:
                data1 = json.load(file1)  
            with open("../FinalDictionary.json") as file2:
                data2 = json.load(file2)     
            data3 = Tools.mergeDicts(data1,data2)           
            with open("../FinalDictionary.json", 'w') as final:         
                final.write(json.dumps(data3,sort_keys=True))        

    def mergeDicts(dict1,dict2):
        dict3 = defaultdict(list)
        for k, v in chain(dict1.items(),dict2.items()):
            if k in dict3 :
                dict3[k][0].extend(v[0])
                dict3[k][1] += v[1] 
            else :  
                dict3[k].append(v[0])
                dict3[k].append(v[1])
                dict3[k].append(v[2])
                # dict[k]
            # print(k )
            # print(v)
            # break
        return dict3      

    def getTermFrequency(term, docId, files):
        doc = Tools.getDocById(docId, files)
        # print(doc)
        tokens = Tokenizer.tokenize(doc) 
        # print(tokens)
        docCount = len(tokens)
        wordCount = 0
        for word in tokens:
            if word == term : 
                wordCount += 1
        if wordCount == 0 : return 0
        # print(wordCount)
        # print(docCount)
        return wordCount/docCount 


    def getDocById(docId, files):
        for filename in files :
            with open("../Dumps/" + filename) as fp:
                data = fp.read()    
            soup = BeautifulSoup(data, "xml")
            documents = soup.find_all("document")
            for document in documents:
                id = int(document["id"])
                if int(id) == int(docId) : 
                    return document.get_text()
        return ""
                    
    def getDocCount (files):
        docCount = 0
        for filename in files :
            with open("../Dumps/"  + filename) as fp:
                data = fp.read()    
            soup = BeautifulSoup(data, "xml")
            documents = soup.find_all("document")    
            docCount += len(documents)
        return docCount

    def getDocFrequency (term, invertedIndex, files):
        docCount = Tools.getDocCount(files)
        docFrequency = invertedIndex[term][1]
        # print("docCount" + str(docCount))
        # print("docFrequency" + str(docFrequency))
        
        return docCount/docFrequency


    def tf_idf(term,docId,invertedIndex , files ) : 
        tf = Tools.getTermFrequency(term, docId, files)
        if tf == 0 : tf = 1
        else : tf = 1 + log(Tools.getTermFrequency(term, docId, files)) 
        idf = log (Tools.getDocFrequency(term, invertedIndex, files))
        return tf*idf

    def loadDictionary(filename):
        with open(filename) as f:
            dictionary = json.load(f)  
        return dictionary


    def sentiment(document):
        afinn = Afinn()
        sentiment = 0 
        tokens = Tokenizer.tokenize(document)
        for token in tokens:
            sentiment += afinn.score(token)
        return sentiment

