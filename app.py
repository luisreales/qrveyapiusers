import os
import pandas as pd 
import numpy as np
from flask import Flask,request,Response,jsonify, render_template, make_response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
from collections import OrderedDict 
from excel import generate_excel
from pdf import generate_pdf_new



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dbUser:72335224*@cluster0.azcfn.mongodb.net/qrvey?retryWrites=true&w=majority"
mongo = PyMongo(app)


# Endpoint: /users
# Description: Return list of users in the dbMongo
# Method: Post
# Developer Created: Luis R
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users
    users_list = []
    for item in users.find():
            users_list.append({'name': item['name'],'username':item['username'],'email': item['email'],'company': item['company'] })

    response = json_util.dumps(users_list)
    return Response(response,mimetype='application/json')


# Endpoint: /users
# Description: Create list of users in the dbMongo
# Method: Post
# Developer Created: Luis R

@app.route('/users', methods=['POST'])
def create_user():   
  
    name = request.json['name']
    username = request.json['username']
    email = request.json['email']
    company = request.json['company']
    
 
    
    if name and username and email:
        id = mongo.db.users.insert({'name':name,'username': username,'email': email,'company':company } )
        response = jsonify({
            '_id': str(id),
            'name': name,
            'username': username,
            'email': email,
            'company': company
        })
       
        response.status_code = 201
        return response
    else:
        return not_found()


# Endpoint: /users/{id}
# Description: Update list of users in the dbMongo
# Method: Post
# Developer Created: Luis R

@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):   
   
   
    
    name = request.json['name']
    username = request.json['username']
    email = request.json['email']
    company = request.json['company']

    if name and username and email and company and _id:

        mongo.db.users.update_one(
                {'_id':ObjectId(_id)},{'$set': {
                'name': name,
                'username': username,
                'email': email,
                'company': company
            }}
        )

        response = jsonify({'message': 'User '+ _id + ' was updated successfully'})
        response.status_code = 200
        return response

    
    else:
        return not_found()


# Endpoint: /users/{id}
# Description: Delete a user by id
# Method: DELETE
# Developer Created: Luis R

@app.route('/users/<_id>', methods=['DELETE'])
def delete_user(_id):
    user_exist = mongo.db.users.find_one({'_id': ObjectId(_id)})
    if user_exist :
        user = mongo.db.users.delete_one({'_id': ObjectId(_id)})
        response = jsonify({'message': 'User '+ _id + ' was deleted successfully'})
        response.status_code = 200
        return response
    else:
        return not_found()

    

# Endpoint: /users/exportExcel
# Description: Generate Excel from dbUsers
# Method: DELETE
# Developer Created: Luis R

@app.route("/exportExcel", methods=['GET'])
def export_records_excel():
    print('llego')
    users = list(mongo.db.users.find({}, {'_id':0,'name':1, 'username':1,'email':1, 'position':'$company.position' }))    
    # Columns
    title = [("name", "name"),("username", "username"),("email", "email"), ("position", "position")]
    filename = 'UsersData.xlsx'    
    return generate_excel(title, users, filename)



# Endpoint: /users/exportExcel
# Description: Generate PDF from dbUsers
# Method: DELETE
# Developer Created: Luis R
#     
@app.route("/exportPDF", methods=['GET'])
def export_records_pdf():
    
  
    users = list(mongo.db.users.find({}, {'_id':0,'name':1, 'username':1,'email':1, 'position':'$company.position' }))    

    # Name of the file
    columns = [['name','username','email','position']]

    user_frame = pd.DataFrame(users).to_numpy()
    array_list = np.append(columns,user_frame,axis=0)
    lista = array_list.tolist()
    doc_pdf = generate_pdf_new(lista)
    response = Response()
    filename = 'ReportUsers.pdf'
    response.data = doc_pdf
    response.headers.add("Content-Type", "application/pdf")
    response.headers.add('Content-Disposition', 'attachment', filename=filename.encode("utf-8").decode("latin1"))
   
    return response



@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":   
    app.run(debug=True)
    