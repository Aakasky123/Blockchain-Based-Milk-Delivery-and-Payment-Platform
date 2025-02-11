from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
import json
from web3 import Web3, HTTPProvider
import time

global details
details = ''
global collector

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'MilkContract.json' #milk contract code
    deployed_contract_address = '0x871FE89C6E45FaBb97cBd94b6Bec69F85Ad5aAaa' #hash address to access student contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'staff':
        details = contract.functions.getNadafaStaff().call()
    if contract_type == 'milk':
        details = contract.functions.getMilkDelivery().call()    
    if len(details) > 0:
        if 'empty' in details:
            details = details[5:len(details)]
    return details     


def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'MilkContract.json' #milk contract file
    deployed_contract_address = '0x871FE89C6E45FaBb97cBd94b6Bec69F85Ad5aAaa' #milk contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'staff':
        details+=currentData
        msg = contract.functions.addNadafaStaff(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'milk':
        details+=currentData
        msg = contract.functions.addMilkDelivery(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    
def AddStaff(request):
    if request.method == 'GET':
       return render(request, 'AddStaff.html', {})

def AddFarmer(request):
    if request.method == 'GET':
       return render(request, 'AddFarmer.html', {})    

def Logout(request):
    if request.method == 'GET':
       return render(request, 'index.html', {}) 

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})    

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def StaffLogin(request):
    if request.method == 'GET':
       return render(request, 'StaffLogin.html', {})

def FarmerLogin(request):
    if request.method == 'GET':
       return render(request, 'FarmerLogin.html', {})    

def AdminLoginAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid Login'}
            return render(request, 'AdminLogin.html', context)

def AddDelivery(request):
    if request.method == 'GET':
        readDetails('staff')
        arr = details.split("\n")
        output = '<TD>&nbsp;&nbsp;<select name="t1">'
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == "farmer":
                output += '<option value="'+array[1]+'">'+array[1]+"</option>"
        output += "</select>"
        context= {'data1':output}
        return render(request, "AddDelivery.html", context)

def ViewFarmerDelivery(request):
    if request.method == 'GET':
        global collector
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Farmer Name','Milk Price','Quantity','Delivery Date','NADAFA Staff Name','Total Amount']
        output += "<tr>"
        amount = 0
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('milk')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == collector:
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+str((float(array[1]) * float(array[2])))+"</td>"
                amount = amount + (float(array[1]) * float(array[2]))
        output += "<tr><td>"+font+"Total Amount = "+str(amount)+"</td>"        
        context= {'data':output}        
        return render(request, 'ViewFarmerDeliveryDetails.html', context)    

def ViewDelivery(request):
    if request.method == 'GET':
        readDetails('staff')
        arr = details.split("\n")
        output = '<TD>&nbsp;&nbsp;<select name="t1">'
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == "farmer":
                output += '<option value="'+array[1]+'">'+array[1]+"</option>"
        output += "</select>"
        context= {'data1':output}
        return render(request, "ViewDelivery.html", context)

def ViewDeliveryAction(request):
    if request.method == 'POST':
        farmer = request.POST.get('t1', False)
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Farmer Name','Milk Price','Quantity','Delivery Date','NADAFA Staff Name','Total Amount']
        output += "<tr>"
        amount = 0
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('milk')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == farmer:
                output += "<tr><td>"+font+array[0]+"</td>"
                output += "<td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+str((float(array[1]) * float(array[2])))+"</td>"
                amount = amount + (float(array[1]) * float(array[2]))
        output += "<tr><td>"+font+"Total Amount = "+str(amount)+"</td>"        
        context= {'data':output}        
        return render(request, 'ViewDetails.html', context) 

def AddDeliveryAction(request):
    if request.method == 'POST':
        global details, collector
        farmer = request.POST.get('t1', False)
        price = request.POST.get('t2', False)
        qty = request.POST.get('t3', False)
        today = str(date.today())
        data = farmer+"#"+price+"#"+qty+"#"+today+"#"+collector+"\n"
        saveDataBlockChain(data,"milk")
        context = {"data":"Milk delivery details added in Blockchain"}
        return render(request, 'AddDelivery.html', context)
        
def FarmerLoginAction(request):
    if request.method == 'POST':
        global collector
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        readDetails('staff')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'farmer' and array[1] == username and array[2] == password:
                status = "success"
                collector = username
                break
        if status == "success":
            context= {'data':'Welcome '+username}
            return render(request, "FarmerScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'FarmerLogin.html', context)


def StaffLoginAction(request):
    if request.method == 'POST':
        global collector
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        readDetails('staff')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == 'staff' and array[1] == username and array[2] == password:
                status = "success"
                collector = username
                break
        if status == "success":
            context= {'data':'Welcome '+username}
            return render(request, "StaffScreen.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'StaffLogin.html', context)

def AddStaffAction(request):
    if request.method == 'POST':
        global details
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        readDetails('staff')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username:
                status = user+" Username already exists"
                break
        if status == "none":
            data = "staff#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"staff")
            context = {"data":"Staff details added in Blockchain"}
            return render(request, 'AddStaff.html', context)
        else:
            context = {"data":status}
            return render(request, 'AddStaff.html', context)


def AddFarmerAction(request):
    if request.method == 'POST':
        global details
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        readDetails('staff')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username:
                status = user+" Username already exists"
                break
        if status == "none":
            data = "farmer#"+username+"#"+password+"#"+contact+"#"+email+"#"+address+"\n"
            saveDataBlockChain(data,"staff")
            context = {"data":"Farmer details added in Blockchain"}
            return render(request, 'AddFarmer.html', context)
        else:
            context = {"data":status}
            return render(request, 'AddFarmer.html', context)

def ViewFarmer(request):
    if request.method == 'GET':
        global details
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Username','Password','Contact No','Email','Address','Record Type']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('staff')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == "farmer":
                output += "<tr><td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
                output += "<td>"+font+"Farmer"+"</td>"
        context= {'data':output}        
        return render(request, 'ViewFarmer.html', context)            

def ViewStaff(request):
    if request.method == 'GET':
        global details
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="white">'
        arr = ['Username','Password','Contact No','Email','Address','Record Type']
        output += "<tr>"
        for i in range(len(arr)):
            output += "<th>"+font+arr[i]+"</th>"
        readDetails('staff')
        arr = details.split("\n")
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == "staff":
                output += "<tr><td>"+font+array[1]+"</td>"
                output += "<td>"+font+array[2]+"</td>"
                output += "<td>"+font+array[3]+"</td>"
                output += "<td>"+font+array[4]+"</td>"
                output += "<td>"+font+array[5]+"</td>"
                output += "<td>"+font+"Staff"+"</td>"
        context= {'data':output}        
        return render(request, 'ViewStaff.html', context)            



        
