import nltk
from afinn import Afinn
from Tokenizer import Tokenizer
import json
import sys
from itertools import chain
from collections import defaultdict

from bs4 import BeautifulSoup


class Indexer(object): 

    def index_document(document,docid):
        tokens = Tokenizer.tokenize(document)
        newtokens = []
        for token in tokens :
            newtokens.append([token,docid])
        return newtokens
        
    def index_file(filename):
        tokens = []
        with open("./input.txt") as fp:
            data = fp.read()    
        soup = BeautifulSoup(data, "xml")
        documents = soup.find_all("document")
        for document in documents:
            id = int(document["id"])
            body = document.get_text()
            url = document["url"]
            tokens.extend(Indexer.index_document(body,id))          
        Indexer.index(tokens)
            
    def index(tokens):
        afinn = Afinn()
        #print(len(tokens))  
        fileCounter = 0    
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

            length = len(postings_list)
            Indexer.addToList(postings_list,token[1])
            if(length != len(postings_list)): 
                postingCount = postingCount + 1

        Tools.saveObject(dictionary,"Minidict" +str(fileCounter)+ ".json" )
        fileCounter = fileCounter+1
        dictionary = {}
        print("Postings Count : "+ str(postingCount))
        print("Term Count : "+ str(dictionaryCount))
        return fileCounter


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

class Tools(object): 

    def saveObject(dictionary,fileName):
        with open(fileName, 'w') as file:
            file.write(json.dumps(dictionary,sort_keys=True))   
        print("File : " + fileName + " saved! ")
