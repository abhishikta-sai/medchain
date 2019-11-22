from flask import Flask,jsonify,request
import requests 
from web3 import Web3
import json
import time
import pandas

url = "http://localhost:8545"
web3  = Web3(Web3.HTTPProvider(url))
mnf_json = []
hc = dict()
hc["Save-a-life Solutions"] = 0
hc["Pro-Medical Solutions"] = 1
hc["Med-Awesome Solutions"] = 2
with open("build/contracts/Admin.json") as f:
    admin_json = json.load(f)

with open("build/contracts/Manufacture.json") as f:
    mnf_json.append(json.load(f))

with open("build/contracts/Manufacture1.json") as f:
    mnf_json.append(json.load(f))

with open("build/contracts/Manufacture2.json") as f:
    mnf_json.append(json.load(f))

with open("build/contracts/Wholesaler.json") as f:
    ws_json = json.load(f)

with open("build/contracts/Customer.json") as f:
    cust_json = json.load(f)

Admin_address = '0x7ef506Ae6A7BB45E2FC2878a7a18bc56eaB7Dbd8'
mnf_address = ['0x8Af5da2797D7833d76be446AD05688AF46798EcF','0x8201f7d5C795e608Bf3cB79e62F564ffBae01f9C','0x892214cA4631C807c983648e8d7Db984902ed389']
ws_address = '0x69e83ACF17B18FC6Ca8421A13Db88c4bbf65EDed'

mnf = []
for i in range(0,3):
    mnf.append(web3.eth.contract(address=mnf_address[i], abi=mnf_json[i]['abi']))
web3.eth.defaultAccount = web3.eth.accounts[0]
admin = web3.eth.contract(address=Admin_address, abi=admin_json['abi'])
ws = web3.eth.contract(address=ws_address, abi=ws_json['abi'])

def addfromcsv_to_bc():
    df = pandas.read_csv("./Data/data.csv")
    for row in df.itertuples():
        tx_hash = mnf[int(hc[str(row.Manufacturer)])].functions.addMedicineRecord(str(row.Manufacturer),int(0),int(row.Quantity),str(row.Name),str(row._4),str(row._5)).transact()
        tx_hash2 = web3.eth.waitForTransactionReceipt(tx_hash)

if(admin.functions.recordCount().call()<10):
    addfromcsv_to_bc()

print(admin.functions.recordCount().call())
app = Flask(__name__)



@app.route("/manaddmedicines" , methods=['POST'])
def addmedicines():
    records = request.form
    tx_hash = mnf[int(records['man_id'])].functions.addMedicineRecord(str(records['man_name']),int(0),int(records['quantity']),str(records['med_name']),records['man_date'],records['exp_date']).transact()
    tx_hash2 = web3.eth.waitForTransactionReceipt(tx_hash)
    print(tx_hash)
    return jsonify({'hash':str(tx_hash)}),200

@app.route("/admin/getmandetails" , methods=['POST'])
def getmandetails():
    recordCount = admin.functions.recordCount().call()
    comp_record = dict()
    j = 0
    man_name = request.form['man_name']
    for i in range(0,recordCount):
        x = admin.functions.records(i).call()
        if(x[2]==man_name):
            temp_rec = dict()

            temp_rec['man_address'] = x[1]
            temp_rec['man_name'] = x[2]
            temp_rec['med_id'] = x[3]
            temp_rec['quantity'] = x[4]
            temp_rec['batch_no'] = str(x[5])
            temp_rec['med_name'] = x[7]
            temp_rec['pkd_date'] = x[8]
            temp_rec['exp_date'] = x[9]
            comp_record[str(j)] = temp_rec
            j = j+1
    #print(comp_record)
    return jsonify(comp_record),200


@app.route("/wsbuymedicines" , methods=['POST'])
def wsbuymedicines():
    records = request.form
    tx_hash = ws.functions.buyMedicine(int(request.form['man_id']),str(records['med_name']),int(records['quantity'])).transact()
    tx_hash2 = web3.eth.waitForTransactionReceipt(tx_hash)
    return jsonify({'hash':str(tx_hash)}),200

if __name__ == '__main__':
	app.run(host="127.0.0.1" ,port=8000, debug = True)