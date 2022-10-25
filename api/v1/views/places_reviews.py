#!/usr/bin/python3
"""
review api request methods
"""

from models.review import Review
from . import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def r_all(place_id):
    """
    Get all reviews of a place
    """
    from models import storage
    from models.place import Place
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    li_reviews = [review.to_dict() for review in reviews]
    return jsonify(li_reviews), 200


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def r_id(review_id):
    """
    Get review with the passed id
    """
    from models import storage
    review = storage.get(Review, review_id)
    print(review)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_r_id(review_id):
    """
    Delete review with the passed id
    """
    from models import storage
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def r_create(place_id):
    """
    Create a review
    """
    from models import storage
    from models.place import Place
    from models.user import User
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        if 'user_id' not in data:
            abort(400, {'message': 'Missing user_id'})
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)

        if 'text' not in data:
            abort(400, {'message': 'Missing text'})
        else:
            data['place_id'] = place_id
            obj = Review(**data)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    else:
        abort(400, {'message': 'Not a JSON'})


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def r_update(review_id):
    """
    Update a review
    """
    from models import storage
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        for key, value in data.items():
            if (key != "id" and key != "created_at" and
                key != "updated_at" and key != "place_id" and
                    key != "user_id"):
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 200
    abort(400, {'message': 'Not a JSON'})
