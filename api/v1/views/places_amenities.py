#!/usr/bin/python3
"""
handle places_amenities relationships
"""

from models.amenity import Amenity
from . import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def pa_all(place_id):
    """
    Get all amenities of a place
    """
    from models import storage
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    li_amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(li_amenities), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def pa_delete(place_id, amenity_id):
    """
    Delete an amenity of a place
    """
    from models import storage
    from models import storage_t
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenities = place.amenities
    if amenity not in amenities:
        abort(404)
    if storage_t != 'db':
        if amenity.id in place.amenity_ids:
            place.amenity_ids.remove(amenity.id)
    else:
        amenities.remove(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['POST'])
def pa_link(place_id, amenity_id):
    """
    Link an amenity to a place
    """
    from models import storage
    from models import storage_t
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenities = place.amenities
    if amenity in amenities:
        return jsonify(amenity.to_dict())
    if storage_t != 'db':
        if amenity.id not in place.amenity_ids:
            place.amenities(amenity)
    else:
        amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
