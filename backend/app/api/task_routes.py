# app/api/task_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.services.xp_service import add_xp
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
  task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

  if not task:
    return jsonify({"error": "Task not found or unauthorized"}), 403
  
  return jsonify([{"id": task.id, "name": task.name, "completed": task.completed} for task in tasks]), 200

# Update a task (Only if User Owns It)
@task_bp.route("/<int:task_id>", methods=["PATCH"])
@jwt_required()
def update_task(task_id):
  current_user_id = get_jwt_identity()
  task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

  if not task:
    return jsonify({"error": "Task not found or unauthorized"}), 403

  data = request.get_json()
  if "name" in data:
    task.name = data["name"]

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

# Create a task (Only if User Owns It)
@task_bp.route("/create", methods=["POST"])
@jwt_required()
def create_task():
  data = request.get_json()

  # Debugging print
  print("Received data:", data, type(data))

  if not data or "name" not in data or not isinstance(data["name"], str):
    return jsonify({"error": "Task name is required and must be a string"}), 400
  
  current_user_id = get_jwt_identity()

  new_task = Task(name=data["name"], user_id=current_user_id)
  db.session.add(new_task)
  db.session.commit()
  return jsonify({"message": "Task created!", "task": {"id": new_task.id, "name": new_task.name}}), 201

# Update task status (Only if User Owns It)
@task_bp.route("/status/<int:task_id>", methods=["PATCH"])
@jwt_required()
def change_task_status(task_id):
  """Allows users to mark a task as complete/incomplete BUT prevents XP farming."""
  current_user_id = get_jwt_identity()
  task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

  if not task:
    return jsonify({"error": "Task not found or unauthorized"}), 403
  
  # Toggle task completion status
  task.completed = not task.completed # Reverse the boolean value

  db.session.commit()
  return jsonify({"message": "Task status updated!", "task": {"id": task.id, "name": task.name, "completed": task.completed}}), 200

# Complete a task and update XP system
@task_bp.route("/complete/<int:task_id>", methods=["POST"])
@jwt_required()
def complete_task(task_id):
  """API endopoint to mark a task as completed and award XP."""
  current_user_id = get_jwt_identity()
  task = Task.query.filter_by(id=task_id, user_id=current_user_id).first()

  if not task:
    return jsonify({"error": "Task not found or unauthorized"}), 403
    
  if task.completed:
    return jsonify({"message": "Task already completed"}), 400
    
  # Mark task as completed
  task.completed = True
  db.session.commit() # Save task completion
  print("success mark task as completed")
  # Award XP to the user
  user = User.query.get(current_user_id)
  if not user:
    return jsonify({"error": "User not found"}), 404

  xp_amount = 10 # Default XP for now (later use AI to determine)
  add_xp(user, xp_amount) # Award XP and check for level-up

  return jsonify({
    "message": "Task completed!",
    "task": {"id": task.id, "name": task.name, "completed": task.completed},
    "xp_awarded": xp_amount,
    "new_xp": user.xp,
    "new_level": user.level
  }), 200
