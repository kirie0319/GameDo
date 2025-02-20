# app/api/task_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.tasks import Task

task_bp = Blueprint("task_bp", __name__)

# Get all tasks (Only User's Own Tasks)
@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
  current_user_id = get_jwt_identity()
  tasks = Task.query.filter_by(user_id=current_user_id).all()
  return jsonify([{"id": task.id, "name": task.name, "completed": task.completed} for task in tasks]), 200

# Get a single task (Only if User Owns It)
@task_bp.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
  current_user_id = get_jwt_identity()
  tasks = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

  if not task:
    return jsonify({"error": "Task not found or unauthorized"}), 403
  
  return jsonify([{"id": task.id, "name": task.name, "completed": task.completed} for task in tasks]), 200

# Update a task (Only if User Owns It)
@task_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
  current_user_id = get_jwt_identity()
  task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

  if not task:
    return jsonify({"error": "Task not found or unauthorized"}), 403

  data = request.get_json()
  if "name" in data:
    task.name = data["name"]
  if "completed" in data:
    task.completed = data["completed"]

  db.session.commit()
  return jsonify({"message": "Task updated!", "task": {"id": task.id, "name": task.name, "completed": task.completed}}), 200

# Delete a task (Only if User Owns It)
@task_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
  current_user_id = get_jwt_identity()
  task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

  if not task:
    return jsonify({"error": "Task not found or unauthorized"}), 403

  db.session.delete(task)
  db.session.commit()
  return jsonify({"message": "Task deleted successfully!"}), 200

@task_bp.route("/create", methods=["POST"])
@jwt_required()
def create_task():
  data = request.get_json()

  # Debugging print
  print("Received data:", data, type(data))

  if not data or "name" not in data or not isinstance(data["name"], str):
    return jsonify({"error": "Task name is repuired and must be a string"}), 400
  
  current_user_id = get_jwt_identity()

  new_task = Task(name=data["name"], user_id=current_user_id)
  db.session.add(new_task)
  db.session.commit()
  return jsonify({"message": "Task created!", "task": {"id": new_task.id, "name": new_task.name}}), 201