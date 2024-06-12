import json
from flask import request, jsonify, abort
from app import app, mongo
from bson.objectid import ObjectId
from functools import wraps
import numpy as np

# Basic Authentication Decorator
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != "user" or auth.password != "password":
            return abort(401)
        return func(*args, **kwargs)
    return wrapper

# Bisection method implementation
def bisection_method(func, a, b, tol):
    def f(x):
        return eval(func)
    
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")
    
    mid = (a + b) / 2.0
    while (b - a) / 2.0 > tol:
        if f(mid) == 0:
            return mid
        elif f(a) * f(mid) < 0:
            b = mid
        else:
            a = mid
        mid = (a + b) / 2.0
    
    return mid

@app.route('/bisection', methods=['POST'])
@authenticate
def create_bisection():
    data = request.get_json()
    if not data or 'function' not in data or 'interval' not in data or 'tolerance' not in data:
        abort(400, description="Invalid data")
    
    func = data['function']
    a, b = data['interval']
    tol = data['tolerance']
    
    try:
        root = bisection_method(func, a, b, tol)
    except ValueError as e:
        abort(400, description=str(e))
    
    result = {
        'function': func,
        'interval': [a, b],
        'tolerance': tol,
        'root': root
    }
    
    db_result = mongo.db.bisections.insert_one(result)
    return jsonify({'id': str(db_result.inserted_id), 'result': result}), 201

@app.route('/bisection/<id>', methods=['GET'])
@authenticate
def get_bisection(id):
    data = mongo.db.bisections.find_one({'_id': ObjectId(id)})
    if not data:
        abort(404, description="Calculation not found")
    
    return jsonify(data), 200

@app.route('/bisection/<id>', methods=['PUT'])
@authenticate
def update_bisection(id):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid data")
    
    existing_data = mongo.db.bisections.find_one({'_id': ObjectId(id)})
    if not existing_data:
        abort(404, description="Calculation not found")
    
    func = data.get('function', existing_data['function'])
    a, b = data.get('interval', existing_data['interval'])
    tol = data.get('tolerance', existing_data['tolerance'])
    
    try:
        root = bisection_method(func, a, b, tol)
    except ValueError as e:
        abort(400, description=str(e))
    
    updated_data = {
        'function': func,
        'interval': [a, b],
        'tolerance': tol,
        'root': root
    }
    
    mongo.db.bisections.update_one({'_id': ObjectId(id)}, {'$set': updated_data})
    return jsonify({'message': 'Calculation updated successfully', 'result': updated_data}), 200

@app.route('/bisection/<id>', methods=['DELETE'])
@authenticate
def delete_bisection(id):
    result = mongo.db.bisections.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        abort(404, description="Calculation not found")
    
    return jsonify({'message': 'Calculation deleted successfully'}), 200
