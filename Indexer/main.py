from Indexer import Indexer
from ranker import Ranker
from Indexer import Tools


def demo(index,files) : 
    
    while True :
        query = input("Please enter search query: ")
        print ("you entered", query)
        if(query == "exit;") : break
        #************************************************************
        #DO SOMETHING WITH THE QUERY HERE
        #Example : 

        result = Ranker.exec_query(query, index, files) 

        #************************************************************
        

        #************************************************************
        #PRINT RESULTS HERE
        #Example : 
        
        print(result[1])

        #************************************************************


#************************************************************
#REQUIRED INITIAL VARAIABLES : 

index = Ranker.open_json("FinalDictionary.json")
files = ["1.txt","2.txt"]

#************************************************************


#************************************************************
#RUN THE DEMO : 

demo(index,files)

#************************************************************





