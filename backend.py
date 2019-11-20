from flask import Flask,jsonify
import json
import re
import requests 
import hashlib
import os
from web3 import Web3
import json

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
    try:
        records = request.get_json()
        tx_hash = mnf.functions.addMedicineRecord(records['med_id'],records['quantity'],records['med_name'],records["man_date"],records["exp_date"]).transact()

        batch_no = web3.eth.waitForTransactionReceipt(tx_hash)
        return json.dumps([batch_no]),200
    except:
        return "error",500

@app.route("/admin/getmandetails" , methods=['POST'])
def getmandetails():
    try:
        man_address = request.get_json()
        tx_hash = admin.functions.sendManDetails(man_address).transact()
        records = web3.eth.waitForTransactionReceipt(tx_hash)
        return json.dumps(records),200
    except:
        return "error",500

if __name__ == '__main__':
	app.run(host="127.0.0.1" ,port=5000, debug = True)
