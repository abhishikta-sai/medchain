import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["medchain"]
mycol = mydb["data"]

myquery = {"Name": "Lexapro"}
newvalues = {"$set": { "Quantity": 1000}}

mycol.update_one(myquery, newvalues)
