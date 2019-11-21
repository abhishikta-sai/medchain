from lxml import html
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import wikipedia

client = MongoClient('localhost', 27017)
db = client.medchain

collection = db.drugs


def get_wiki_summary(page_soup):
    summary = ""
    paragraphs = page_soup.findAll()
    for paragraph in paragraphs:
        if paragraph.name == "p":
            print(paragraph)
            links = paragraph.findAll('a')
            print("Links:")
            print(links)
            summary += paragraph.text + " "
            print("Adding summary")
            break
        elif paragraph.name == "div" and paragraph.has_attr('class') and paragraph['class'][0] == 'toc':
            break	
    
    print(summary)
    return summary
    

def get_wiki_company_categories(page_soup):
    categories = []
    table_html = str(page_soup.find("table", {"class":"infobox vcard"}))
    if table_html == "None":
        print("Returning none")	
        return categories
    soup_table = BeautifulSoup(table_html, 'html.parser')
    td_list = soup_table.findAll("td", {"class":"category"})
    
    for item in td_list:
	    if item.previous_sibling != None and item.previous_sibling.text == "Industry":
	        a_tag_list = BeautifulSoup(str(item), 'html.parser').findAll("a")
	        for tag in a_tag_list:
		        categories.append(tag.text)
    
    print(categories)
    return categories


def get_wiki_company_suggestions(page_title):
    suggestions = wikipedia.search(page_title)
    return suggestions[0]


def get_wiki_info(page_title):	
    '''print(page_title)
    response = requests.get("https://en.wikipedia.org/wiki/"+page_title)
    if response.status_code != 200:
        suggestion = get_wiki_company_suggestions(page_title)
        if suggestion == None:
            return [""]
        response = requests.get("https://en.wikipedia.org/wiki/"+suggestion)     	

    page_html = response.content
    page_soup = BeautifulSoup(page_html, 'html.parser')
    
    summary = get_wiki_summary(page_soup)

    return [summary]'''
    print(page_title)
    try:
        page = wikipedia.page(page_title)
    except:
        print("None")
        return ""
    print(page.summary)
    print(page.links[:10])    
    return page.summary

file = open("drugs.txt",'r')
lines = file.readlines()
companies = [i.replace("\n","") for i in lines]
insert_docs = []

for company in companies:
    summary = get_wiki_info(company)
    insert_docs.append({"Name":company, "Summary":summary})

# result = collection.insert_many(insert_docs)
# print("Done")

# print(get_wiki_info("ThoughtSpot"))