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
collection = db.readlist
# Select the collection


@app.route("/api/v1/readbook/<int:user_id>", methods=['GET'])
def get_user_readlist(user_id):
    """
       Function to obtain the list of readed books.
       """
    try:        
        user_id = int(user_id)
        data = collection.find({"user_id": user_id})
        if data.count() > 0:
            return dumps(data[0]),200
        else:
            # Return empty array if no list or user are found
            return jsonify([]),200
    except:        
        return "", 500

@app.route("/api/v1/readbook/<int:user_id>/<int:book>", methods=['PUT'])
def add_book_readlist(user_id,book):
    """
       Function to add a book.
       """
    try:        
        user_id = int(user_id)
        data = collection.find({"user_id": user_id})

        if data.count() > 0:            
            bk = data[0]['books']
            
            if int(book) in bk:
                return jsonify({"Error":"Book alredy in the list"}),409

            bk.append(int(book))

            try:
                collection_readbooks.update_one({"user_id": user_id},{"$set":{"books":bk}})
            except: 
                # Bad request
                return jsonify({"Error":"Not Acceptable (Invalid Params)"}), 406
            return "",200

        else:

            data = {"user_id" : user_id,"books": [book]}
            record_created = collection.insert(data)

            return "", 200

    except:        
        return "", 500


