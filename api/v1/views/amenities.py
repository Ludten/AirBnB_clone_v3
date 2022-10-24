#!/usr/bin/python3
"""
amenity api request methods
"""

from models.amenity import Amenity
from . import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def a_all():
    """
    Get all amenities
    """
    from models import storage
    amenities = storage.all(Amenity)
    li_amenities = [v.to_dict() for k, v in amenities.items()]
    return jsonify(li_amenities), 200


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def a_id(amenity_id):
    """
    Get amenity with the passed id
    """
    from models import storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_a_id(amenity_id):
    """
    Delete amenity with the passed id
    """
    from models import storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def a_create():
    """
    Create a amenity
    """
    from models import storage
    data = request.get_json(silent=True)
    if data:
        if 'name' in data:
            obj = Amenity(**data)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
        else:
            abort(400, {'message': 'Missing name'})
    else:
        abort(400, {'message': 'Not a JSON'})


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def a_update(amenity_id):
    """
    Update a amenity
    """
    from models import storage
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        for key, value in data.items():
            if (key != "id" and key != "created_at" and key != "updated_at"):
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    abort(400, {'message': 'Not a JSON'})
