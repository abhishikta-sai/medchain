from flask import Flask, render_template, flash, request, session, redirect, url_for, make_response, jsonify
from flask_restful import Resource, Api
import requests
import json
from forms import *

import spacy
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'this is the end'
api = Api(app)
url = 'http://127.0.0.1:8000'

hc = dict()
hc["Save-a-life Solutions"] = 0
hc["Pro-Medical Solutions"] = 1
hc["Med-Awesome Solutions"] = 2


client = MongoClient('localhost', 27017)
db = client.medchain

data_collection = db.data
collection = db.drugs


class Index(Resource):
    def get(self):
        return redirect(url_for('admin'))


api.add_resource(Index, '/')


class Admin(Resource):
    def get(self):
        return make_response(render_template('admin.html'))

    def post(self):
        y = {'man_name':request.form.get('manufacturer_option')}
        res = requests.post(url + '/admin/getmandetails', data=y)
        # res is a dictionary of dictionaries, where the keys are indexes
        #print(res.json())
        return jsonify(res.json())


api.add_resource(Admin, '/admin')


class Manufacturer(Resource):
    def get(self):
        return make_response(render_template('manufacturer.html')) 

    def post(self):
        print("hi")
        x = {'man_id': hc[request.form['man_name']], 'man_name': request.form['man_name'], 'med_id': request.form['med_id'], 'med_name': request.form['med_name'], 'quantity': request.form['quantity'], 'man_date': datetime.strftime(request.form['man_date']), 'exp_date': datetime.strftime(request.form['exp_date'])}
        res = requests.post(url + '/manaddmedicines', data=x)
        print(res['hash']) # byte 32
        return jsonify(res)
        # returns a Batch Number


api.add_resource(Manufacturer, '/manufacturer')


class Wholesaler(Resource):
    def get(self):
        return make_response(render_template('wholesaler.html'))

    def post(self):
        x = {'man_id': hc[request.form['man_name']],
             'man_name': request.form['man_name'],
             'med_name': request.form['med_name'],
             'med_id': request.form['med_id'],
             'quantity': request.form['quantity'], }
        print(x)
        res = requests.post(url + '/wsbuymedicines', data=x)
        print(res['hash']) # byte 32
        return jsonify(res)


api.add_resource(Wholesaler, '/wholesaler')


class WholesalerData(Resource):
    def get(self):
        med_names = {}
        for item in data_collection.find():
            med_names[item['Name']] = item['Name']
        return jsonify(med_names)

    def post(self):
        drug = request.form.get('drug')
        print(drug)
        med_names = []
        man_names = []
        quantity = []
        man_date = []
        exp_date = []
        for item in data_collection.find():
            med_names.append(item['Name'])
            man_names.append(item['Manufacturer'])
            quantity.append(item['Quantity'])
            man_date.append(item['Manufacturing Date'])
            exp_date.append(item['Expiry Date'])
        res = []
        for i in range(len(med_names)):
            if med_names[i] == drug:
                d = {}
                d['Manufacturer'] = man_names[i]
                d['Quantity'] = quantity[i]
                d['ManufacturingDate'] = man_date[i]
                d['ExpiryDate'] = exp_date[i]
                res.append(d)
        return jsonify(res)


api.add_resource(WholesalerData, '/wholesalerdata')


class DrugSearch(Resource):
    def get(self):
        return make_response(render_template('drugsearch.html'))

    def post(self):
        drug = request.form.get('drug')
        print(drug)
        med_names = []
        man_names = []
        quantity = []
        for item in data_collection.find():
            med_names.append(item['Name'])
            man_names.append(item['Manufacturer'])
            quantity.append(item['Quantity'])
        res = {}
        res['Save-a-life Solutions'] = 0
        res['Pro-Medical Solutions'] = 0
        res['Med-Awesome Solutions'] = 0
        for i in range(len(med_names)):
            if med_names[i] == drug:
                if man_names[i] == 'Save-a-life Solutions':
                    res['Save-a-life Solutions'] += quantity[i]
                elif man_names[i] == 'Pro-Medical Solutions':
                    res['Pro-Medical Solutions'] += quantity[i]
                elif man_names[i] == 'Med-Awesome Solutions':
                    res['Med-Awesome Solutions'] += quantity[i]
        return jsonify(res)


api.add_resource(DrugSearch, '/drugsearch')


class SearchFieldView(Resource):
    def get(self):
        form = SearchForm()
        return make_response(render_template('search.html'))


api.add_resource(SearchFieldView, '/search')


class SearchResultPage(Resource):
    def get(self):
        search_request = request.args.get("search_field")
        session["search_query"] = search_request
        print(session["search_query"])
        return make_response(render_template('results.html', result={"search_query": session["search_query"]}))


api.add_resource(SearchResultPage, '/searchresultpage')

nlp = spacy.load("en_core_web_md")


class SearchMedicines(Resource):
    global nlp
    api_name = "Search Company api"
    tag_objects = []
    names = []
    summaries = []
    categories = []
    for item in collection.find():
        names.append(item["Name"])
        summaries.append(item["Summary"])
        tag_objects.append(nlp(" ".join(item["Tags"].split(","))))

    def get(self):
        search_request_object = nlp(request.args.get("search_field"))
        similarities = []
        for i in range(len(self.tag_objects)):
            similarities.append([self.names[i].replace(u'\u2013', '-'), self.summaries[i].replace(u'\u2013', '-'),
                                 self.tag_objects[i].similarity(search_request_object)])
        similarities.sort(key=lambda x: x[2], reverse=True)
        similarities = similarities[0:5]
        session["search_results"] = similarities
        return jsonify(
            search_results=similarities
        )


api.add_resource(SearchMedicines, '/searchMedicines')


if __name__ == '__main__':
    app.run(debug = True)
