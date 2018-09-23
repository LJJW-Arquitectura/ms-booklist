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

@app.route("/")
def get_initial_response():
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'API BookList'
    }
    resp = jsonify(message)
    return resp


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
            date_creation = str(datetime.datetime.now().time())
            date_update = date_creation
            
            if collection.find({'name': name,'user_id': user_id,}).count() > 0:
                # List alredy exists
                return jsonify({"Error":"List alredy exists"}), 409
            
        except:
            # Bad request
            return jsonify({"Error":"Bad request"}), 400

        record_created = collection.insert({'name': name,
            'user_id': user_id,
            'user': user,
            'date_creation': date_creation,
            'date_update': date_update,
            'books':books})
        # Return Id 
        return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        return "", 500

@app.route("/api/v1/booklist/<user_id>/<name>/<book>", methods=['POST'])
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
            date_update = str(datetime.datetime.now().time())

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

@app.route("/api/v1/booklist", methods=['GET'])
def get_all_booklist():
    """
       Function to get all the list.
       """
    try:        
        # Return all the records as query string parameters are not available
        data = collection.find()
        if data.count() > 0:
            # Prepare response if the users are found
            return dumps(data),200
        else:
            # Return empty array if no users are found
            return jsonify([])
    except:        
        return "", 500

@app.route("/api/v1/booklist/<user_id>", methods=['GET'])
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

@app.route("/api/v1/booklist/<user_id>/<name>", methods=['GET'])
def get_booklist(user_id,name):
    """
       Function to get one list.
       """
    try:        
        user_id = int(user_id)
        data = collection.find({"user_id": user_id,"name":name})
        if data.count() > 0:
            return dumps(data),200
        else:
            # Return empty array if no list are found
            return "",406
    except:        
        return "", 500



@app.route("/api/v1/booklist/<user_id>/<name>", methods=['PUT'])
def update_booklist(user_id,name):
    """
       Function to update the user.
       """
    try:
        # Get the value which needs to be updated
        try:
           
            try:
                new_name = request.json['new_name']
            except:
                new_name = name

            if not(isinstance(new_name, str)) or not (isinstance(name, str)) or not(isinstance(int(user_id),int)):
                raise
            books = request.json['books']
            for bk in books:
                if not(isinstance(bk,int)):
                    raise
            books = list(set(books))
            date_update = str(datetime.datetime.now().time())
            if new_name != name and collection.find({'name': new_name,'user_id': user_id,}).count() > 0:
                # List alredy exists
                return jsonify({"Error":"Name alredy exists"}), 409
            
        except:
            # Bad request
            return jsonify({"Error":"Bad request"}), 400

        # Updating

        records_updated = collection.update_one( {"user_id": int(user_id),"name":str(name)} , {"$set":{'name': new_name,
            'date_update': date_update,
            'books':books}})
        
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


@app.route("/api/v1/booklist/<user_id>/<name>", methods=['DELETE'])
def remove_booklist(user_id,name):
    """
       Function to remove the booklist.
       """
    try:
        # Delete the booklist

        delete = collection.delete_one({"user_id": int(user_id),"name": str(name)})

        if delete.deleted_count > 0 :
            # Prepare the response
            return "", 204
        else:
            # Resource Not found
            return "Resource Not found", 404
    except:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        return "", 500


@app.errorhandler(404)
def page_not_found(e):
    """Send message to the user with notFound 404 status."""
    # Message to the user
    message = {
        "err":
            {
                "msg": "This route is currently not supported. Please refer API documentation."
            }
    }
    # Making the message looks good
    resp = jsonify(message)
    # Sending OK response
    resp.status_code = 404
    # Returning the object
    return resp
