#!/usr/bin/python3
"""
state api request methods
"""

from models.state import State
from . import app_views
from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def s_all():
    """
    Get all states
    """
    from models import storage
    states = storage.all(State)
    li_states = [v.to_dict() for k, v in states.items()]
    return jsonify(li_states), 200


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def s_id(state_id):
    """
    Get state with the passed id
    """
    from models import storage
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def del_s_id(state_id):
    """
    Delete state with the passed id
    """
    from models import storage
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def s_create():
    """
    Create a state
    """
    from models import storage
    data = request.get_json(silent=True)
    if data:
        if 'name' in data:
            obj = State(**data)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
        else:
            abort(400, {'message': 'Missing name'})
    else:
        abort(400, {'message': 'Not a JSON'})


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def s_update(state_id):
    """
    Update a state
    """
    from models import storage
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data:
        for key, value in data.items():
            if (key != "id" and key != "created_at" and key != "updated_at"):
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    abort(400, {'message': 'Not a JSON'})
