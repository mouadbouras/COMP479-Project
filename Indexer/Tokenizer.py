import nltk
from nltk.corpus import stopwords
import codecs, sys, glob, os, unicodedata


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
