from Indexer import Indexer
from ranker import Ranker
from Indexer import Tools


def demo(index,files, topx) : 
    
    while True :
        query = input("Please enter search query: ")
        print ("you entered", query)
        if(query == "exit;") : break
        #************************************************************
        #DO SOMETHING WITH THE QUERY HERE
        #Example : 

        result = Ranker.exec_query(query, index, files) 

        #************************************************************
        # Call ranking class to organize results
        resultIDs = Ranker.do_ranking(query, result[0], files, topx)

        #************************************************************
        #PRINT RESULTS HERE
        #Example : 
        
        print("Ranked Results : ")
        print(resultIDs)

        #************************************************************


#************************************************************
#REQUIRED INITIAL VARAIABLES : 

index = Ranker.open_json("FinalDictionary.json")
files = ["1.txt","2.txt"] #<=========  has to contain the list of documents you want to index [corpus]
topx = 50

#************************************************************


#************************************************************
#RUN THE DEMO : 

demo(index,files, topx)

#************************************************************


#************************************************************
#BUILD INDEX : 

#to build the index uncomment the following line 

# index_files(files, True)

#************************************************************



