from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

from app import booklistsController
from app import readedbooklistsController

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


@app.route("/")
def get_initial_response():
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'API BookList'
    }
    return jsonify(message)