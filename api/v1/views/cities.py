#!/usr/bin/python3
"""
city api request methods
"""

from models.city import City
from . import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def c_all(state_id):
    """
    Get all cities of a state
    """
    from models import storage
    from models.state import State
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    li_cities = [city.to_dict() for city in cities]
    return jsonify(li_cities), 200


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def c_id(city_id):
    """
    Get city with the passed id
    """
    from models import storage
    city = storage.get(City, city_id)
    print(city)
    if city:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_c_id(city_id):
    """
    Delete city with the passed id
    """
    from models import storage
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def c_create(state_id):
    """
    Create a city
    """
    from models import storage
    from models.state import State
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        if 'name' in data:
            data['state_id'] = state_id
            obj = City(**data)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
        else:
            abort(400, {'message': 'Missing name'})
    else:
        abort(400, {'message': 'Not a JSON'})


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def c_update(city_id):
    """
    Update a city
    """
    from models import storage
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        for key, value in data.items():
            if (key != "id" and key != "created_at" and
                    key != "updated_at" and key != "state_id"):
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    abort(400, {'message': 'Not a JSON'})
