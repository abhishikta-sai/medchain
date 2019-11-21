from flask import Flask,jsonify,request
import json
import re
import requests 
import hashlib
import os
from web3 import Web3
import json
import time

url = "http://localhost:8545"
web3  = Web3(Web3.HTTPProvider(url))

with open("build/contracts/Admin.json") as f:
    admin_json = json.load(f)

with open("build/contracts/Manufacture.json") as f:
    mnf_json = json.load(f)

with open("build/contracts/Wholesaler.json") as f:
    ws_json = json.load(f)

with open("build/contracts/Customer.json") as f:
    cust_json = json.load(f)

Admin_address = '0x7ef506Ae6A7BB45E2FC2878a7a18bc56eaB7Dbd8'
mnf_address = '0x8Af5da2797D7833d76be446AD05688AF46798EcF'
ws_address = '0x8201f7d5C795e608Bf3cB79e62F564ffBae01f9C'
cust_address = '0x892214cA4631C807c983648e8d7Db984902ed389'

web3.eth.defaultAccount = web3.eth.accounts[0]
admin = web3.eth.contract(address=Admin_address, abi=admin_json['abi'])
mnf = web3.eth.contract(address=mnf_address, abi=mnf_json['abi'])
ws = web3.eth.contract(address=ws_address, abi=ws_json['abi'])
cust = web3.eth.contract(address=cust_address, abi=cust_json['abi'])

app = Flask(__name__)

@app.route("/manaddmedicines" , methods=['POST'])
def addmedicines():
    records = request.form
    tx_hash = mnf.functions.addMedicineRecord(int(records['med_id']),int(records['quantity']),str(records['med_name']),records["man_date"],records["exp_date"]).transact()
    tx_hash2 = web3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_hash)
    #batch_no = admin.functions.batch_no().call()
    return jsonify({'hash':str(tx_hash)}),200
    '''except:
        return "error",500'''

@app.route("/admin/getmandetails" , methods=['POST'])
def getmandetails():
    recordCount = admin.functions.recordCount().call()
    comp_record = dict()
    j = 0
    man_address = eval(request.data)[0]
    for i in range(0,recordCount):
        x = admin.functions.records(i).call()
        if(x[1]==man_address):
            temp_rec = dict()

            temp_rec['man_address'] = x[1]
            temp_rec['med_id'] = x[2]
            temp_rec['quantity'] = x[3]
            temp_rec['batch_no'] = str(x[4])
            temp_rec['med_name'] = x[7]
            temp_rec['pkd_date'] = x[8]
            temp_rec['exp_date'] = x[9]
            comp_record[str(j)] = temp_rec
            print(type(x[4]))
            j = j+1
    return jsonify(comp_record),200

if __name__ == '__main__':
	app.run(host="127.0.0.1" ,port=8000, debug = True)