#!/usr/bin/python3
"""
place api request methods
"""

from models.amenity import Amenity
from models.city import City
from models.place import Place
from . import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def p_all(city_id):
    """
    Get all places of a city
    """
    from models import storage
    from models.city import City
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    li_places = [place.to_dict() for place in places]
    return jsonify(li_places), 200


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def p_id(place_id):
    """
    Get place with the passed id
    """
    from models import storage
    place = storage.get(Place, place_id)
    print(place)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_p_id(place_id):
    """
    Delete place with the passed id
    """
    from models import storage
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def p_create(city_id):
    """
    Create a place
    """
    from models import storage
    from models.city import City
    from models.user import User
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        if 'user_id' not in data:
            abort(400, {'message': 'Missing user_id'})
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        if 'name' not in data:
            abort(400, {'message': 'Missing name'})
        else:
            data['city_id'] = city_id
            obj = Place(**data)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    else:
        abort(400, {'message': 'Not a JSON'})


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def p_update(place_id):
    """
    Update a place
    """
    from models import storage
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        for key, value in data.items():
            if (key != "id" and key != "created_at" and
                key != "updated_at" and key != "city_id" and
                    key != "user_id"):
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    abort(400, {'message': 'Not a JSON'})


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def placesearch():
    """
    Update a place
    """
    from models import storage
    from models.state import State
    from models.city import City
    data = request.get_json(silent=True)
    if data:
        if data == {} or all([v == [] for k, v in data.items()]):
            places = storage.all(Place)
            li_places = [v.to_dict() for k, v in places.items()]
            return jsonify(li_places), 200
        pslist = []
        if 'states' in data and data['states'] != []:
            for state_id in data['states']:
                state = storage.get(State, state_id)
                for city in state.cities:
                    pslist.extend(city.places)
        if 'cities' in data and data['cities'] != []:
            for city_id in data['cities']:
                city = storage.get(City, city_id)
                for place in city.places:
                    if place not in pslist:
                        pslist.append(place)
        if 'amenities' in data and data['amenities'] != []:
            amenitylist = [storage.get(Amenity, amenity_id)
                           for amenity_id in data['amenities']]
            for place in pslist:
                if all(amenity in place.amenities
                       for amenity in amenitylist) is False:
                    pslist.remove(place)
        li_places = [place.to_dict() for place in pslist]
        return jsonify(li_places), 200
    else:
        abort(400, {'message': 'Not a JSON'})
