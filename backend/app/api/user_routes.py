# app/api/user_routes.py
from flask import Blueprint, jsonify
from app.models.user import User

user_bp = Blueprint("user_bp", __name__) # Create Blueprint

@user_bp.route("/", methods=["GET"])
def get_users():
  users = User.query.all()
  return jsonify([user.to_dict() for user in users]), 200

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
  user = User.query.get_or_404(user_id)
  return jsonify(user.to_dict()), 200