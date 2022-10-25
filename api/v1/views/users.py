#!/usr/bin/python3
"""
user api request methods
"""

from models.user import User
from . import app_views
from flask import jsonify, abort, request


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def u_all():
    """
    Get all users
    """
    from models import storage
    users = storage.all(User)
    li_users = [v.to_dict() for k, v in users.items()]
    return jsonify(li_users), 200


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def u_id(user_id):
    """
    Get user with the passed id
    """
    from models import storage
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_u_id(user_id):
    """
    Delete user with the passed id
    """
    from models import storage
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def u_create():
    """
    Create a user
    """
    from models import storage
    data = request.get_json(silent=True)
    if data:
        if 'email' not in data:
            abort(400, {'message': 'Missing email'})
        if 'password' not in data:
            abort(400, {'message': 'Missing password'})
        else:
            obj = User(**data)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    else:
        abort(400, {'message': 'Not a JSON'})


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def u_update(user_id):
    """
    Update a user
    """
    from models import storage
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        for key, value in data.items():
            if (key != "id" and key != "created_at" and
                    key != "updated_at" and key != 'email'):
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    abort(400, {'message': 'Not a JSON'})
