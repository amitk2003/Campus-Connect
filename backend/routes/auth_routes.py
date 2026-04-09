from flask import Blueprint, request, jsonify
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import datetime
import random
import string

def generate_anon_name():
    return "User#" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

auth_bp = Blueprint('auth', __name__)
users_collection = db['Users']

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('role'):
        return jsonify({"message": "Missing required fields"}), 400
        
    existing_user = users_collection.find_one({"email": data['email']})
    if existing_user:
        return jsonify({"message": "User already exists"}), 400
        
    if data['role'].lower() == 'admin':
        existing_admin = users_collection.find_one({"role": {"$regex": "^admin$", "$options": "i"}})
        if existing_admin:
            return jsonify({"message": "Admin already exists. Only one Admin is allowed."}), 400
        
    hashed_password = generate_password_hash(data['password'])
    new_user = {
    "name": data.get('name', ''),
    "email": data['email'],
    "password": hashed_password,
    "role": data['role'],
    "anon_name": generate_anon_name(),  # ✅ ADD THIS
    "created_at": datetime.datetime.utcnow()
}
    
    users_collection.insert_one(new_user)
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing email or password"}), 400
        
    user = users_collection.find_one({"email": data['email']})
    if not user or not check_password_hash(user['password'], data['password']):
        return jsonify({"message": "Invalid email or password"}), 401
        
    access_token = create_access_token(identity=str(user['_id']), additional_claims={"role": user['role']})
    return jsonify(
        access_token=access_token,
        user_id=str(user['_id']),
        role=user['role'],
        name=user.get('anon_name', 'User')  # Use anon_name as the display name
    ), 200