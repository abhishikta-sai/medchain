from flask import Flask, render_template, flash, request, session, redirect, url_for, make_response, jsonify
from flask_restful import Resource, Api
import requests
import json
from forms import *

import spacy
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'this is the end'
api = Api(app)
url = 'localhost:8000'

client = MongoClient('localhost', 27017)
db = client.medchain

collection = db.drugs

class Index(Resource):
    def get(self):
        return redirect(url_for('admin'))

api.add_resource(Index, '/')

class Admin(Resource):
    def get(self):
        return make_response(render_template('admin.html'))
        
api.add_resource(Admin, '/admin')

class GetManDetails(Resource):
    def post(self):
        res = requests.post(url + '/admin/getmandetails', request.form.get('manufacturer_option'))
        print(res)
        return res

api.add_resource(GetManDetails, '/getmandetails')

class Manufacturer(Resource):
    def get(self):
        return make_response(render_template('manufacturer.html')) 
    # def post(self):
    #     request.post(url + '/manaddmedicine', {'man_id': ,'med_id': ,'quantity': ,'med_name': ,'man_date': ,'exp_date': })
        # returns a Batch Number

api.add_resource(Manufacturer, '/manufacturer')

class WholesalerPage(Resource):
    def get(self):
        return make_response(render_template('wholesaler.html'))

api.add_resource(WholesalerPage, '/wholesaler')

class WholesalerData(Resource):
    def get(self):
        request.get(url + '/')
        return make_response(200)
    def post(self):
        request.post(url + '/')
        return make_response(200)

api.add_resource(WholesalerData, '/wholesalerdata')

class Customer(Resource):
    def get(self):
        return make_response(render_template('customer.html'))
    # def post(self):

api.add_resource(Customer, '/customer')


class SearchFieldView(Resource):
    def get(self):
        form = SearchForm()	
        return make_response(render_template('search.html')) 
api.add_resource(SearchFieldView, '/search')

class SearchResultsPage(Resource):
    def get(self):
        print(session["search_query"])
       	print(session["search_results"])
        return make_response(render_template('results.html', result={"search_query": session["search_query"], "search_results": session["search_results"]})) 

api.add_resource(SearchResultsPage, '/searchresultpage')


class SearchMedicines(Resource):
    api_name = "Search Company api"
    tag_objects = []
    nlp = spacy.load("en_core_web_md")
    names = []
    summaries = []
    categories = []
    for item in collection.find():
        names.append(item["Name"])
        summaries.append(item["Summary"])
        tag_objects.append(nlp(" ".join(item["Tags"].split(","))))

    def get(self):
        print(self.api_name)
        search_request = request.args.get("search_field")
        print(search_request)
        search_request_object = self.nlp(search_request)
        similarities = []
        for i in range(len(self.tag_objects)):
            similarities.append([self.names[i].replace(u'\u2013', '-'), self.summaries[i].replace(u'\u2013', '-'),
                                 self.tag_objects[i].similarity(search_request_object)])
        similarities.sort(key=lambda x: x[2], reverse=True)
        similarities = similarities[0:5]
        session["search_query"] = search_request.replace(u'\u2013', '-')
        session["search_results"] = similarities
        return redirect(url_for('searchresultspage'))


api.add_resource(SearchMedicines, '/searchMedicines')
    
    

class Statistics(Resource):
    def get(self):
        pass    	
        



    
if __name__ == '__main__':
	app.run()