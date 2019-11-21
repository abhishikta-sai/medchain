import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.medchain

collection = db.drugs


def f1(string):
    return re.search('\[[0-9]+\]', string)


def get_wiki_info(page_title):
    response = requests.get("https://en.wikipedia.org/wiki/"+page_title)
    if response.status_code != 200:
        return ""
    page_html = response.content
    page_soup = BeautifulSoup(page_html, 'html.parser')
    paragraphs = page_soup.find_all('p')
    names = []
    summary = ""
    for i in range(2):
        links = paragraphs[i].find_all('a')
        for link in links:
            if not f1(link.text):
               names.append(link.text)
        summary += paragraphs[i].text
    result = ",".join(names)
    print(result)
    print(summary)
    return [result, summary]


file = open("drugs.txt",'r')
lines = file.readlines()
companies = [i.replace("\n","") for i in lines]
insert_docs = []

for company in companies:
    result, summary = get_wiki_info(company)
    insert_docs.append({"Name":company, "Summary":summary, "Tags": result})

result = collection.insert_many(insert_docs)
print("Done")

# print(get_wiki_info("ThoughtSpot"))