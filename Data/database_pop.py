import pandas as pd
from pymongo import MongoClient
import string


df = pd.read_csv("data.csv")
print(df.columns)

client = MongoClient('localhost', 27017)
db = client.medchain
collection = db.data
collection.drop()
collection = db.data
collection.insert_many(df.to_dict('records'))