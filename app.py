import json
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import sqlite3

app = Flask(__name__)
api = Api(app)

class GetAndCreateAContact(Resource):
    def get(self):
        contacts_list = []
        with sqlite3.connect("contacts.db") as conn:
            c = conn.cursor()            
            for row in c.execute("SELECT * FROM contacts"):
                contacts_list.append({"id": row[0],"name": {"first": row[1],"middle": row[2],"last": row[3]},"address": {"street": row[4],"city": row[5],"state": row[6],"zip": row[7]},"phone": {"number": row[8],"type": row[9]},"email": row[10]})
        return contacts_list    
    
    def post(self):
        id_num = request.json['id']
        first = request.json['name']['first']
        middle = request.json['name']['middle']
        last = request.json['name']['last']
        street = request.json['address']['street']
        city = request.json['address']['city']
        state = request.json['address']['state']
        zip_num = request.json['address']['zip']
        
        number = request.json['phone']['number']
        phone_type = request.json['phone']['type']
        email = request.json['email']
            
        with sqlite3.connect("contacts.db") as conn:
           c = conn.cursor()
           create_table = """CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, first text, middle text, last text, street text, city text, state text, zip text, number text, type text, email text)"""
           c.execute(create_table)

           c.execute("""INSERT INTO contacts (id,first,middle,last,street,city,state,zip,number,type,email) 
              VALUES (?,?,?,?,?,?,?,?,?,?,?)""",(id_num,first,middle,last,street,city,state,zip_num,number,phone_type,email)) 
           conn.commit()
          
        return {"message": "Stored successfully"}, 200

class GetAndEditContact(Resource):
    def get(self,id_num):
        contacts_list = []
        with sqlite3.connect("contacts.db") as conn:
            c = conn.cursor()            
            for row in c.execute("SELECT * FROM contacts WHERE id = ?",(id_num,)):
                contacts_list.append({"id": row[0],"name": {"first": row[1],"middle": row[2],"last": row[3]},"address": {"street": row[4],"city": row[5],"state": row[6],"zip": row[7]},"phone": {"number": row[8],"type": row[9]},"email": row[10]})
        return contacts_list 
    
    def put(self,id_num):
        with sqlite3.connect("contacts.db") as conn:                
            c = conn.cursor()
            #Validating Information from Request
            if type(request.json['name']['first']) == str:
                first = request.json['name']['first']                
            else:
                return {"message": "Invalid first name"}                
            if type(request.json['name']['middle']) == str:
                middle = request.json['name']['middle']
            else:
                return {"message": "Invalid middle name"}   
            if type(request.json['name']['last']) == str:
                last = request.json['name']['last']
            else:
                return {"message": "Invalid last name"} 
            if type(request.json['address']['street']) == str:
                street = request.json['address']['street']
            else:
                return {"message": "Invalid street name"}
            if type(request.json['address']['city']) == str:
                city = request.json['address']['city']
            else:
                return {"message": "Invalid city name"}
            if type(request.json['address']['state']) == str:
                state = request.json['address']['state']
            else:
                return {"message": "Invalid state name"}
            if type(request.json['address']['zip']) == str:
                zip_num = request.json['address']['zip']
            else:
                return {"message": "Invalid zip code"}
            if type(request.json['phone']['number']) == str:
                number = request.json['phone']['number']
            else:
                return {"message": "Invalid phone number"}
            if type(request.json['phone']['type']) == str:
                phone_type = request.json['phone']['type']
            else:
                return {"message": "Invalid phone type"}
            if type(request.json['email']) == str:
                email = request.json['email']
            else:
                return {"message": "Invalid email"}
            query = "UPDATE contacts SET first = ?,middle = ?,last = ?,street = ?,city = ?,state = ?,zip = ?,number = ?,type = ?,email = ? WHERE id =?"
            values = (first,middle,last,street,city,state,zip_num,number,phone_type,email,id_num)
            c.execute(query, values)
            conn.commit()         
            return {'message': 'Successfully updated'}   
    
    def delete(self,id_num):
        with sqlite3.connect("contacts.db") as conn:
            c = conn.cursor()                
            query = "DELETE FROM contacts WHERE id = ?"
            c.execute(query,(id_num,))
            return {'Message': 'Contact was deleted'}

class GetContactlistForHomePhones(Resource):
   def get(self,):
        contacts_list = []
        with sqlite3.connect("contacts.db") as conn:
            c = conn.cursor()           
            for row in c.execute("SELECT * FROM contacts WHERE type = 'Home'"):
                contacts_list.append({"id": row[0],"name": {"first": row[1],"middle": row[2],"last": row[3]},"address": {"street": row[4],"city": row[5],"state": row[6],"zip": row[7]},"phone": {"number": row[8],"type": row[9]},"email": row[10]})
            sort_by_last = sorted(contacts_list, key = lambda i: i['name']['last'])
            
        return sorted(sort_by_last,key = lambda i:i['name']['first'])
        
      
api.add_resource(GetAndCreateAContact, '/contacts')
api.add_resource(GetAndEditContact, '/contacts/<int:id_num>')
api.add_resource(GetContactlistForHomePhones, '/contacts/call-list')

app.run(port = 7000, debug = False)
