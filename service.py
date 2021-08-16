from flask import Flask, request
from flask import jsonify
import mysql.connector
import requests
import json


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="contact_list"

)

app = Flask(__name__)


@app.route('/login-authentication/', methods=['GET'])
def authentication():
    emailId=request.args.get('ID')
    password=request.args.get('password')
  
    print (emailId)
    print (password)

    mycursor = mydb.cursor()
    
    mycursor.execute("SELECT EXISTS(SELECT * FROM credentials WHERE ID = %s AND PASSWORD = %s)",(emailId,password))

    myresult = mycursor.fetchall()
    if(myresult[0][0]==1):
     return "True"
    else:
     return "False"

@app.route('/signup-contact/', methods=['POST'])
def signup():
    emailId=request.args.get('ID')
    passwordId=request.args.get('password')

    mycursor = mydb.cursor()
    #Check if already present
    mycursor.execute("SELECT * FROM credentials WHERE ID = %s",(emailId,))
    myresult = mycursor.fetchall()
    if len(myresult) >0:
     return "False"
    
    sql="INSERT INTO credentials (ID, PASSWORD) VALUES (%s, %s)"
    val = (emailId, passwordId)
    mycursor.execute(sql, val)

    mydb.commit()
    return "True"

@app.route('/fetch-data/', methods=['GET'])
def fetch():
    emailId=request.args.get('ID')
    mycursor = mydb.cursor()
    mycursor.execute("SELECT FirstNm,LastNm,Email,Phone FROM data WHERE ID = %s",(emailId,))
    myresult = mycursor.fetchall()
    print(myresult)
    out=changeMap(myresult)
    #print(out)
    if len(myresult) >0:
        return jsonify(out)

def changeMap(L):
    ListDict=[]
    for list in L:
       Dict ={}
       print (list[0])   
       Dict['First Name']=list[0]
       Dict['Last Name']=list[1]
       Dict['Email']=list[2]
       Dict['Phone']=list[3]
       ListDict.append(Dict)
    return ListDict

@app.route('/create-contact/', methods=['GET'])
def createContact():
    ID=request.args.get('ID')
    FirstName=request.args.get('FirstNm')
    LastNm=request.args.get('LastNm')
    Email=request.args.get('Email')
    Phone=request.args.get('Phone')

    mycursor = mydb.cursor()
    sql="INSERT INTO data (ID,FirstNm,LastNm,Email,Phone) VALUES (%s, %s,%s,%s,%s)"
    val = (ID,FirstName,LastNm,Email,Phone)
    mycursor.execute(sql, val)

    mydb.commit()
    return "True"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)