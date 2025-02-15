from flask import Flask, render_template, request,send_from_directory,send_file
import json
from web3 import Web3, HTTPProvider
import os
import cv2
import datetime
import pyqrcode
import png
from pyqrcode import QRCode
import pickle

app = Flask(__name__)

global details
details=''
global contract

UPLOAD_FOLDER = 'static/uploads/'

def readDetails(contract_type):
    global details
    details = ""
    blockchain_address = 'http://127.0.0.1:8545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Organic.json' 
    deployed_contract_address = '0x04970170DfC82db872aaf0210dabDd876aeFfe60' #hash address to access counter feit contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'Farmer':
        details = contract.functions.getfarmer().call()
    if contract_type == 'distributor':
        details = contract.functions.getdistributor().call()
    if contract_type == 'retailer':
        details = contract.functions.getretailer().call()
    if contract_type == 'customer':
        details = contract.functions.getcustomer().call()
    if contract_type == 'adduser':
        details = contract.functions.getuser().call()
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]    
      

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:8545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Organic.json' 
    deployed_contract_address = '0x04970170DfC82db872aaf0210dabDd876aeFfe60' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'Farmer':
        details+=currentData
        msg = contract.functions.setfarmer(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'distributor':
        details+=currentData
        msg = contract.functions.setdistributor(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'retailer':
        details+=currentData
        msg = contract.functions.setretailer(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'customer':
        details+=currentData
        msg = contract.functions.setcustomer(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'adduser':
        details+=currentData
        msg = contract.functions.setuser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    



@app.route('/AddFarmerAction', methods=['POST'])
def AddFarmerAction():
    if request.method == 'POST':
        global details
        username = request.form['t1']
        password = request.form['t2']
        contact = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        readDetails('adduser')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Farmer' and array[1] == username:
                status = username+" already exists"
                break
        if status == "none":
            data = "Farmer#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"adduser")
            context = "Farmer signup task completed"
            return render_template('FarmerRegister.html', data=context)
        else:
            context = status
            return render_template('FarmerRegister.html', data=context)


@app.route('/AddDistributorAction', methods=['POST'])
def AddDistributorAction():
    if request.method == 'POST':
        global details
        username = request.form['t1']
        password = request.form['t2']
        contact = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        readDetails('adduser')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Distributor' and array[1] == username:
                status = username+" already exists"
                break
        if status == "none":
            data = "Distributor#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"adduser")
            context = "Distributor signup task completed"
            return render_template('DistributorRegister.html', data=context)
        else:
            context = status
            return render_template('DistributorRegister.html', data=context)

@app.route('/AddRetailerAction', methods=['POST'])
def AddRetailerAction():
    if request.method == 'POST':
        global details
        username = request.form['t1']
        password = request.form['t2']
        contact = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        readDetails('adduser')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Retailer' and array[1] == username:
                status = username+" already exists"
                break
        if status == "none":
            data = "Retailer#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"adduser")
            context = "Retailer signup task completed"
            return render_template('RetailerRegister.html', data=context)
        else:
            context = status
            return render_template('RetailerRegister.html', data=context)

@app.route('/AddCustomerAction', methods=['POST'])
def AddCustomerAction():
    if request.method == 'POST':
        global details
        username = request.form['t1']
        password = request.form['t2']
        contact = request.form['t3']
        email = request.form['t4']
        address = request.form['t5']
        readDetails('adduser')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Customer' and array[1] == username:
                status = username+" already exists"
                break
        if status == "none":
            data = "Customer#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"adduser")
            context = "Customer signup task completed"
            return render_template('CustomerRegister.html', data=context)
        else:
            context = status
            return render_template('CustomerRegister.html', data=context)


@app.route('/FarmerLoginAction', methods=['POST'])
def FarmerLoginAction():
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Farmer' and array[1] == username and array[2] == password:
                status = "success"
                break
        if status == "success":
            context = "Welcome " + username
            return render_template('FarmerScreen.html', data=context)
        else:
            context = "Invalid Details"
            return render_template('FarmerLogin.html', data=context)


@app.route('/DistributorLoginAction', methods=['POST'])
def DistributorLoginAction():
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Distributor' and array[1] == username and array[2] == password:
                status = "success"
                break
        if status == "success":
            context = "Welcome " + username
            return render_template('DistributorScreen.html', data=context)
        else:
            context = "Invalid Details"
            return render_template('DistributorLogin.html', data=context)


@app.route('/RetailerLoginAction', methods=['POST'])
def RetailerLoginAction():
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Retailer' and array[1] == username and array[2] == password:
                status = "success"
                break
        if status == "success":
            context = "Welcome " + username
            return render_template('RetailerScreen.html', data=context)
        else:
            context = "Invalid Details"
            return render_template('RetailerLogin.html', data=context)


@app.route('/CustomerLoginAction', methods=['POST'])
def CustomerLoginAction():
    if request.method == 'POST':
        username = request.form['t1']
        password = request.form['t2']
        status = "none"
        readDetails('adduser')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'Customer' and array[1] == username and array[2] == password:
                status = "success"
                break
        if status == "success":
            context = "Welcome " + username
            return render_template('CustomerScreen.html', data=context)
        else:
            context = "Invalid Details"
            return render_template('CustomerLogin.html', data=context)


@app.route('/AddVegetables',methods=['POST'])
def AddVegetables():
    if request.method == 'POST':
        pid = request.form['t1']
        pname = request.form['t2']
        quantity = request.form['t3']
        price = request.form['t4']
        file = request.files['t5']
        filename = file.filename
        print("@@ Input posted = ", filename)
        file_path = os.path.join('static/photo/', filename)
        file.save(file_path)
        status = "none"
        readDetails('Farmer')   
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == pid:
                status = 'Product Id is already Existing'
                return render_template('AddVegetables.html', data=status)
                break

        if status == "none":
            data = pid+"#"+pname+"#"+quantity+"#"+price+"#"+filename+"\n"
            saveDataBlockChain(data,'Farmer')
            context = 'Crop Details Added Successfully.'
            return render_template('AddVegetables.html', data=context)  

def check_distributor(number):
    readDetails('distributor')
    arr = details.split("\n")
    for i in range(len(arr)-1):
        array = arr[i].split("#")
        if array[0] == number:
            return True
            break
    return False

@app.route('/CheckProduct', methods=['GET', 'POST'])
def CheckProduct():
    if request.method == 'GET':
        global number,name,price,photo
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Number', 'Product Name','Quantity in Kg', 'Product Price per kg','Photo' ,'Action']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('Farmer')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            output += '<tr>'
            for cell in array[0:4]:
                output += f'<td>{font}{cell}{font}</td>'
            output += '<td><img src=static/photo/'+array[4]+'  width="200" height="200"></img></td>'   
            action_cell = f'<td><a href="/SubmitDistributor?number={array[0]}&name={array[1]}&quantity={array[2]}&price={array[3]}&photo={array[4]}">{font}Click Here to submit Ingedients{font}</a></td>' if not check_distributor(array[0]) else f'<td>{font}Already Submitted{font}</td>'

            output += action_cell
            output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('CheckProduct.html', data=output)

@app.route('/SubmitDistributor', methods=['GET', 'POST'])
def SubmitDistributor():
    global number,name,quantity,price,photo

    if request.method == 'GET':
        number = request.args.get('number')
        name = request.args.get('name')
        price =  request.args.get('price')
        quantity = request.args.get('quantity')
        photo = request.args.get('photo')
        return render_template('SubmitDistributor.html')

    if request.method == 'POST':
        text = request.form['t1']
        data = number+"#"+name+"#"+price+"#"+quantity+"#"+text+"#"+photo+"\n"
        saveDataBlockChain(data, "distributor")

        context = "Ingedients Saved to blockchain."

        return render_template('SubmitDistributor.html', data=context)


def check_retailer(number):
    readDetails('retailer')
    arr = details.split("\n")
    for i in range(len(arr)-1):
        array = arr[i].split("#")
        if array[0] == number:
            return True
            break
    return False

@app.route('/SellProduct', methods=['GET', 'POST'])
def SellProduct():
    if request.method == 'GET':
        global number,name,price,text,quantity,photo
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Number', 'Product Name','Quantity in Kg', 'Product Price per kg','Ingedients by distributor','Photo' ,'Action']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('distributor')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            output += '<tr>'
            for cell in array[0:5]:
                output += f'<td>{font}{cell}{font}</td>'
            output += '<td><img src=static/photo/'+array[5]+'  width="200" height="200"></img></td>'   
            action_cell = f'<td><a href="/SubmitRetailer?number={array[0]}&name={array[1]}&quantity={array[2]}&price={array[3]}&text={array[4]}&photo={array[5]}">{font}Click Here to sell{font}</a></td>' if not check_retailer(array[0]) else f'<td>{font}Already Sold{font}</td>'

            output += action_cell
            output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('SellProduct.html', data=output)




@app.route('/SubmitRetailer', methods=['GET', 'POST'])
def SubmitRetailer():
    global number,name,price,text,quantity,photo

    if request.method == 'GET':
        number = request.args.get('number')
        name = request.args.get('name')
        price =  request.args.get('price')
        quantity = request.args.get('quantity')
        text = request.args.get('text')
        photo = request.args.get('photo')
        return render_template('SubmitRetailer.html')

    if request.method == 'POST':
        qr_code_path = 'static/qrcode/'+number +'.png'
        if os.path.exists(qr_code_path):
            os.remove(qr_code_path)
        url = pyqrcode.create(number)
        url.png('static/qrcode/'+number+'.png', scale = 6)
        context = "Product details added with id : "+number+"<br/>Download QR CODE"
        data = number+"#"+name+"#"+price+"#"+quantity+"#"+text+"#"+photo+"\n"
        saveDataBlockChain(data, "retailer")
        return send_file(qr_code_path, as_attachment=True)
    return render_template('SubmitRetailer.html', data=context)

@app.route('/AuthenticateScanAction', methods=['GET', 'POST'])
def AuthenticateScanAction():
    if request.method == 'POST':
        barcode = request.files['t1']
        filename = barcode.filename        
        print("@@ Input posted = ", filename)
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        barcode.save(file_path)
        detector = cv2.QRCodeDetector()

        image =cv2.imread(file_path)

        data, bbox, _ = detector.detectAndDecode(image)

        print(data)
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Number', 'Product Name','Quantity in Kg', 'Product Price per kg','Ingedients by distributor','Photo']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('retailer')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")
            if array[0] == data:
                flag = 1
                output += '<tr>'
                for cell in array[0:5]:
                    output += f'<td>{font}{cell}{font}</td>'
                output += '<td><img src=static/photo/'+array[5]+'  width="200" height="200"></img></td>'   
                
                output += '</tr>'

        output += '</table><br/><br/><br/>'
                
        if flag == 0:
            output += "<tr><td>Uploaded Product Barcode Authentication Failed</td></tr>"
        output+="<br/><br/><br/><br/><br/><br/>"
        return render_template('ViewDetails.html', msg=output)

def check_customer(number):
    readDetails('customer')
    arr = details.split("\n")
    for i in range(len(arr)-1):
        array = arr[i].split("#")
        if array[0] == number:
            return True
            break
    return False

@app.route('/BuyProduct', methods=['GET', 'POST'])
def BuyProduct():
    if request.method == 'GET':
        global number,name,price,text,quantity,photo
        output = '<table border="1" align="center" width="100%">'
        font = '<font size="3" color="black">'
        headers = ['Product Number', 'Product Name','Quantity in Kg', 'Product Price per kg','Ingedients by distributor','Photo' ,'Action']

        output += '<tr>'
        for header in headers:
            output += f'<th>{font}{header}{font}</th>'
        output += '</tr>'

        readDetails('retailer')
        arr = details.split("\n")

        for i in range(len(arr) - 1):
            array = arr[i].split("#")

            output += '<tr>'
            for cell in array[0:5]:
                output += f'<td>{font}{cell}{font}</td>'
            output += '<td><img src=static/photo/'+array[5]+'  width="200" height="200"></img></td>'   
            action_cell = f'<td><a href="/SubmitCustomer?number={array[0]}&name={array[1]}&quantity={array[2]}&price={array[3]}&text={array[4]}&photo={array[5]}">{font}Click Here to buy{font}</a></td>' if not check_customer(array[0]) else f'<td>{font}Already Sold{font}</td>'

            output += action_cell
            output += '</tr>'

        output += '</table><br/><br/><br/>'

        return render_template('BuyProduct.html', data=output)


@app.route('/SubmitCustomer', methods=['GET', 'POST'])
def SubmitCustomer():
    global number,name,price,text,quantity,photo

    if request.method == 'GET':
        number = request.args.get('number')
        name = request.args.get('name')
        price =  request.args.get('price')
        quantity = request.args.get('quantity')
        text = request.args.get('text')
        photo = request.args.get('photo')
        return render_template('SubmitCustomer.html')

    if request.method == 'POST':
        pur = request.form['t1']
        data = number+"#"+name+"#"+price+"#"+quantity+"#"+text+"#"+pur+"#"+photo+"\n"
        saveDataBlockChain(data, "customer")

        context = "Purchase Completed Successfully."

        return render_template('SubmitCustomer.html', data=context)


@app.route('/CustomerLogin', methods=['GET', 'POST'])
def CustomerLogin():
    if request.method == 'GET':
       return render_template('CustomerLogin.html', msg='')

@app.route('/CustomerRegister', methods=['GET', 'POST'])
def CustomerRegister():
    if request.method == 'GET':
       return render_template('CustomerRegister.html', msg='')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/BuyProduct', methods=['GET', 'POST'])
def BuyProducts():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/CustomerScreen', methods=['GET', 'POST'])
def CustomerScreen():
    if request.method == 'GET':
       return render_template('CustomerScreen.html', msg='')

@app.route('/DistributorLogin', methods=['GET', 'POST'])
def DistributorLogin():
    if request.method == 'GET':
       return render_template('DistributorLogin.html', msg='')

@app.route('/DistributorRegister', methods=['GET', 'POST'])
def DistributorRegister():
    if request.method == 'GET':
       return render_template('DistributorRegister.html', msg='')

@app.route('/DistributorScreen', methods=['GET', 'POST'])
def DistributorScreen():
    if request.method == 'GET':
       return render_template('DistributorScreen.html', msg='')

@app.route('/FarmerLogin', methods=['GET', 'POST'])
def FarmerLogin():
    if request.method == 'GET':
       return render_template('FarmerLogin.html', msg='')

@app.route('/FarmerRegister', methods=['GET', 'POST'])
def FarmerRegister():
    if request.method == 'GET':
       return render_template('FarmerRegister.html', msg='')

@app.route('/FarmerScreen', methods=['GET', 'POST'])
def FarmerScreen():
    if request.method == 'GET':
       return render_template('FarmerScreen.html', msg='')

@app.route('/RetailerLogin', methods=['GET', 'POST'])
def RetailerLogin():
    if request.method == 'GET':
       return render_template('RetailerLogin.html', msg='')

@app.route('/RetailerRegister', methods=['GET', 'POST'])
def RetailerRegister():
    if request.method == 'GET':
       return render_template('RetailerRegister.html', msg='')

@app.route('/RetailerScreen', methods=['GET', 'POST'])
def RetailerScreen():
    if request.method == 'GET':
       return render_template('RetailerScreen.html', msg='')

@app.route('/AddVegetables', methods=['GET', 'POST'])
def AddVegetabless():
    if request.method == 'GET':
       return render_template('AddVegetables.html', msg='')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
       return render_template('index.html', msg='')

@app.route('/SubmitDistributor', methods=['GET', 'POST'])
def SubmitDistributors():
    if request.method == 'GET':
       return render_template('SubmitDistributor.html', msg='')

@app.route('/CheckProduct', methods=['GET', 'POST'])
def CheckProducts():
    if request.method == 'GET':
       return render_template('CheckProduct.html', msg='')

@app.route('/SellProduct', methods=['GET', 'POST'])
def SellProducts():
    if request.method == 'GET':
       return render_template('SellProduct.html', msg='')

@app.route('/SubmitRetailer', methods=['GET', 'POST'])
def SubmitRetailers():
    if request.method == 'GET':
       return render_template('SubmitRetailer.html', msg='')

@app.route('/AuthenticateScan', methods=['GET', 'POST'])
def AuthenticateScans():
    if request.method == 'GET':
       return render_template('AuthenticateScan.html', msg='')

@app.route('/ViewDetails', methods=['GET', 'POST'])
def ViewDetailss():
    if request.method == 'GET':
       return render_template('ViewDetails.html', msg='')

if __name__ == '__main__':
    app.run()  