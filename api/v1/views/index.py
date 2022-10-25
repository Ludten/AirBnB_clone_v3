#!/usr/bin/python3
"""
api request methods
"""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from . import app_views
from flask import jsonify

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """
    A function for routing status requests
    """
    return jsonify(
        {
            "status": "OK"
        }
    )


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    A function for routing object stats requests
    """
    from models import storage

    return jsonify(
        {
            "amenities": storage.count(Amenity),
            "cities": storage.count(City),
            "places": storage.count(Place),
            "reviews": storage.count(Review),
            "states": storage.count(State),
            "users": storage.count(User)
        }
    )
