from Indexer import Indexer
        

Indexer.index_files(["input.txt"],True)


# for z in range (0,22):
#     ss = ""
#     if z < 10: ss = "0"
#     with open("./reuters21578/reut2-0"+ss+str(z)+".sgm") as fp:
#         data = fp.read()    
#         data = data[:35] + "<ROOT>" + data[35:] + "</ROOT>"
#     soup = BeautifulSoup(data, "xml")

#     reuters = soup.find_all('REUTERS')

#     for j in range (0 , len(reuters)):
#         id = int(reuters[j]["NEWID"])
#         # print(reuters[j].BODY)
#         if not reuters[j].BODY : continue  
#         title =  reuters[j].TITLE                 
#         body = reuters[j].BODY
#         # print(body.string)
#         s = title.string.strip()
#         s += " " + body.string.strip()
#         tokens.extend(tokenize(s,id))