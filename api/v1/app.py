#!/usr/bin/python3
"""
HBnB flask Application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask import render_template
from models import storage
from os import getenv
from .views import app_views

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle error 404
    """
    return jsonify(
        {
            "error": "Not found"
        }
    ), 404


@app.errorhandler(400)
def custom400(error):
    """
    Handle error 400
    """
    response = jsonify({'error': error.description['message']})
    return response


@app.teardown_appcontext
def teardown_db(exception):
    """What to do at the end of session"""
    storage.close()


if __name__ == '__main__':
    if getenv('HBNB_API_HOST'):
        HBNB_API_HOST = getenv('HBNB_API_HOST')
    else:
        HBNB_API_HOST = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        HBNB_API_PORT = getenv('HBNB_API_PORT')
    else:
        HBNB_API_PORT = '5000'
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
