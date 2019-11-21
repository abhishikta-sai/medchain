from flask import Flask, render_template, flash, request, session, redirect, url_for, make_response, jsonify
from flask_restful import Resource, Api
import requests
import json
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


class Index(Resource):
    def get(self):
        return redirect(url_for('admin'))

api.add_resource(Index, '/')


class Admin(Resource):
    def get(self):
        return make_response(render_template('admin.html'))
    def post(self):
        res = requests.post(url + '/admin/getmandetails', json.dumps([request.form.get('manufacturer_option')]))
        return make_response("hello")


api.add_resource(Admin, '/admin')


class Manufacturer(Resource):
    def get(self):
        return make_response(render_template('manufacturer.html')) 
    def post(self):
        print("hi")
        x = {'man_id':hc[request.form['man_name']],'man_name': request.form['man_name'], 'med_id': request.form['med_id'], 'med_name': request.form['med_name'], 'quantity': request.form['quantity'], 'man_date': datetime.strftime(request.form['man_date']), 'exp_date': datetime.strftime(request.form['exp_date'])}
        res = requests.post(url + '/manaddmedicines', data=x)
        print(res['hash'])
        return make_response("hello")
        # returns a Batch Number


api.add_resource(Manufacturer, '/manufacturer')


class WholesalerPage(Resource):
    def get(self):
        return make_response(render_template('wholesaler.html'))
    def post(self):
        x = {'man_id':hc[request.form['man_name']],
             'man_name': request.form['man_name'],
             'med_name': request.form['med_name'],
             'med_id': request.form['med_id'],
             'quantity': request.form['quantity'],
            }
        print(x)
        res = requests.post(url + '/wsbuymedicines', data=x)
        print(res['hash'])
        return make_response("hello")


api.add_resource(WholesalerPage, '/wholesaler')

# class WholesalerData(Resource):
#     def get(self):
#         request.get(url + '/')
#         return make_response(200)
#     def post(self):
#         request.post(url + '/')
#         return make_response(200)

# api.add_resource(WholesalerData, '/wholesalerdata')


class DrugSearch(Resource):
    def get(self):
        return make_response(render_template('drugsearch.html'))
    # def post(self):

        
api.add_resource(DrugSearch, '/drugsearch')
    
if __name__ == '__main__':
	app.run()