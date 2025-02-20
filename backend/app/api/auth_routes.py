# app/api/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User

auth_bp = Blueprint("auth_bp", __name__)

# User Registration
@auth_bp.route("/register", methods=["POST"])
def register():
  data = request.get_json()

  if not data.get("username") or not data.get("email") or not data.get("password"):
    return jsonify({"error": "All fields are required"}), 400

  # Check if user already exists
  if User.query.filter_by(email=data["email"]).first():
    return jsonify({"error": "Email already exists"}), 400

  new_user = User(username=data["username"], email=data["email"])
  new_user.set_password(data["password"]) # Hash password
  db.session.add(new_user)
  db.session.commit()

  return jsonify({"message": "User registered successfully"}), 201

# User Login (Returns JWT Token)
@auth_bp.route("/login", methods=["POST"])
def login():
  data = request.get_json()

  user = User.query.filter_by(email=data["email"]).first()
  if user and user.check_password(data["password"]):
    access_token = create_access_token(identity=user.id)
    return jsonify({"token": access_token, "message": "Login successful!"}), 200
  
  return jsonify({"error": "Invalid email or password"}), 401

# Protected Route
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
  current_user_id = get_jwt_identity()
  user = User.query.get(current_user_id)

  return jsonify({"message": f"Hello, {user.username}! You have access to this route."}), 200