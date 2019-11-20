from flask import Flask, render_template, flash, request, session, redirect, url_for, make_response
from flask_restful import Resource, Api
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests;
import json;

app = Flask(__name__)
app.secret_key = 'this is the end'
api = Api(app)


class Index(Resource):
    def get(self):
        return redirect(url_for('admin'))

api.add_resource(Index, '/')

class Admin(Resource):
    def get(self):
        return make_response(render_template('admin.html'))

api.add_resource(Admin, '/admin')

class Manufacturer(Resource):
    def get(self):
        return make_response(render_template('manufacturer.html')) 

api.add_resource(Manufacturer, '/manufacturer')

class Wholesaler(Resource):
    def get(self):
        return make_response(render_template('wholesaler.html')) 

api.add_resource(Wholesaler, '/wholesaler')

class Customer(Resource):
    def get(self):
        return make_response(render_template('customer.html')) 

api.add_resource(Customer, '/customer')

    
if __name__ == '__main__':
	app.run()