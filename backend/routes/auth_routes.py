from flask import Blueprint, request, jsonify
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
import random
import string
import secrets

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


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({"message": "Email is required"}), 400
        
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"message": "If this email exists, a reset link will be sent."}), 200
        
    # Generate a secure random token
    reset_token = secrets.token_urlsafe(32)
    expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"reset_token": reset_token, "reset_token_expiry": expiry}}
    )
    
    # In a real app, send an email here. For now, we return it for testing.
    print(f"Password reset token for {email}: {reset_token}")
    
    return jsonify({
        "message": "Reset link sent to your email",
        "debug_token": reset_token  # Remove this in production
    }), 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({"message": "Token and password are required"}), 400
        
    user = users_collection.find_one({
        "reset_token": token,
        "reset_token_expiry": {"$gt": datetime.datetime.utcnow()}
    })
    
    if not user:
        return jsonify({"message": "Invalid or expired token"}), 400
        
    hashed_password = generate_password_hash(new_password)
    users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"password": hashed_password}, "$unset": {"reset_token": "", "reset_token_expiry": ""}}
    )
    
    return jsonify({"message": "Password reset successful"}), 200


@auth_bp.route('/google-login', methods=['POST'])
def google_login():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    google_id = data.get('google_id')
    role = data.get('role', 'Student') # Default role if sign up
    
    if not email:
        return jsonify({"message": "Email is required"}), 400
        
    user = users_collection.find_one({"email": email})
    
    if not user:
        # Create new user for Google Sign In
        if role.lower() == 'admin':
            existing_admin = users_collection.find_one({"role": {"$regex": "^admin$", "$options": "i"}})
            if existing_admin:
                return jsonify({"message": "Admin already exists. Only one Admin is allowed."}), 400
        
        new_user = {
            "name": name,
            "email": email,
            "google_id": google_id,
            "role": role,
            "anon_name": generate_anon_name(),
            "created_at": datetime.datetime.utcnow()
        }
        users_collection.insert_one(new_user)
        user = users_collection.find_one({"email": email})
    
    access_token = create_access_token(identity=str(user['_id']), additional_claims={"role": user['role']})
    return jsonify(
        access_token=access_token,
        user_id=str(user['_id']),
        role=user['role'],
        name=user.get('anon_name', 'User')
    ), 200