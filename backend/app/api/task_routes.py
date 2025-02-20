# app/api/task_routes.py
from flask import Blueprint, jsonify, request
from app import db
from app.models.tasks import Task

task_bp = Blueprint("task_bp", __name__)

@task_bp.route("/", methods=["POST"])
def create_task():
  data = request.get_json()
  if not data or not data.get("name"):
    return jsonify({"error": "Task name is required"}), 400

  new_task = Task(name=data["name"], user_id=data["user_id"])
  db.session.add(new_task)
  db.session.commit()
  return jsonify({"error": "Task created!", "task": {"id": new_task.id, "name": new_task}}), 201