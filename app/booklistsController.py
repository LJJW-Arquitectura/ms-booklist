"""This module will serve the api request."""

from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
import imp
import datetime

# Select the database
db = client.restfulapi
# Select the collection
collection = db.booklist

@app.route("/api/v1/booklist", methods=['POST'])
def create_booklist():
    """
       Function to create new bookslist.
       """       
    try:
        # Create new booklist
        try:           
            
            name = request.json['name']
            user = request.json['user']
            user_id = request.json['user_id']
            if not(isinstance(user, str)) or not (isinstance(name, str)) or not(isinstance(user_id,int)):
                raise 

            books = request.json['books']
            for bk in books:
                if not(isinstance(bk,int)):
                    raise

            books = list(set(books))
            date_creation = str(datetime.date.today() )
            date_update = date_creation
            
            if collection.find({'name': name,'user_id': user_id,}).count() > 0:
                #List alredy exists
                return jsonify({"Error":"List alredy exists"}), 409
            
        except:
            # Bad request
            return jsonify({"Error":"Bad request"}), 400

        data = {'name': name,
            'user_id': user_id,
            'user': user,
            'date_creation': date_creation,
            'date_update': date_update,
            'books':books}

        record_created = collection.insert(data)

        return jsonify({'name': name,
            'user_id': user_id,
            'user': user,
            'date_creation': date_creation,
            'date_update': date_update,
            'books':books}), 201
    except:
        # Error while trying to create the resource
        return "", 500

@app.route("/api/v1/booklist/<user_id>/<name>/<book>", methods=['PUT'])
def add_book(user_id,name,book):
    """
       Function to add a book to a list.
       """
    try:        
        user_id = int(user_id)
        data = collection.find({"user_id": user_id,"name":name})

        if data.count() > 0:
            
            bk = data[0]['books']

            if int(book) in bk:
                return jsonify({"Error":"Book alredy in the list"}),409

            bk.append(int(book))
            date_update = str(datetime.date.today() )

            try:
                collection.update_one({"user_id": user_id,"name":name},{"$set":{"books":bk,"date_update":date_update}})
            except: 
                # Bad request
                return jsonify({"Error":"Not Acceptable (Invalid Params)"}), 406

            return "",200
        else:
            
            # Return empty array if no list are found
            return "",404
    except:        
        return "", 500

#@app.route("/api/v1/booklist/p/<int:page>", methods=['GET'])
#def get_all_booklist(page):

@app.route("/api/v1/booklist/", methods=['GET'])
def get_all_booklist():
    """
       Function to get all the list.
       """
    try:        
        #data = collection.find().skip(int(page*5)).limit(5)
        data = collection.find()
        if data.count() > 0:
            # Prepare response
            return dumps(data),200
        else:
            return jsonify([]),200
    except:        
        return "", 500

@app.route("/api/v1/booklist/<int:user_id>", methods=['GET'])
def get_user_booklist(user_id):
    """
       Function to obtain all the lists of a user.
       """
    try:        
        user_id = int(user_id)
        data = collection.find({"user_id": user_id})
        if data.count() > 0:  
            return dumps(data),200
        else:
            # Return empty array if no list or user are found
            return "",404
    except:        
        return "", 500

@app.route("/api/v1/booklist/<int:user_id>/<name>", methods=['GET'])
def get_booklist(user_id,name):
    """
       Function to get one list.
       """
    try:        
        user_id = int(user_id)
        data = collection.find({"user_id": user_id,"name":name})
        if data.count() > 0:
            return dumps(data[0]),200
        else:
            # Return empty array if no list are found
            return "",406
    except:        
        return "", 500



@app.route("/api/v1/booklist/<int:user_id>/<string:_name>", methods=['PUT'])
def update_booklist(user_id,_name):
    """
       Function to update a booklist.
       """
    try:
        # Get the value which needs to be updated
        try:
           
            if('name' in request.json) :
                new_name = request.json['name']
            else:
                new_name = _name

            if('books' in request.json):
                books = request.json['books']
            else:
                books = []

            if not(isinstance(new_name, str)) or not (isinstance(_name, str)) or not(isinstance(int(user_id),int)):
                raise

            for bk in books:
                if not(isinstance(bk,int)):
                    raise

            books = list(set(books))

            date_update = str(datetime.date.today())
            if new_name != _name and collection.find({'name': new_name,'user_id': user_id,}).count() > 0:
                # List alredy exists
                return jsonify({"Error":"Name alredy exists"}), 409
            
        except:
            # Bad request
            return jsonify({"Error":"Bad request"}), 400

        # Updating

        if('books' in request.json):
            records_updated = collection.update_one( {"user_id": int(user_id),"name":str(_name)} , {"$set":{'name': new_name,
                'date_update': date_update,
                'books':books}})
        else:
            records_updated = collection.update_one( {"user_id": int(user_id),"name":str(_name)} , {"$set":{'name': new_name,
                'date_update': date_update}})

        # Check if resource is updated
        if records_updated.matched_count > 0:
            # Prepare the response as resource is updated successfully
            return "", 204
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "", 404
    except:
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/api/v1/booklist/<int:user_id>/<name>", methods=['DELETE'])
def remove_booklist(user_id,name):
    """
       Function to remove the booklist.
       """
    print(user_id)
    try:
        # Delete the booklist

        delete = collection.delete_one({"user_id": int(user_id),"name": str(name)})

        if delete.deleted_count > 0 :
            # Prepare the response
            return "", 204
        else:
            # Resource Not found
            return jsonify({"Error":"Resource Not found"}), 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500



