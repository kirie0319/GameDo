# app/api/__init__.py
from flask import Blueprint

# Import all Blueprints
from app.api.user_routes import user_bp
from app.api.task_routes import task_bp
from app.api.auth_routes import auth_bp

# Create a main API Blueprint
api_bp = Blueprint("api", __name__)

# Register all Blueprints
api_bp.register_blueprint(user_bp, url_prefix="/users")
api_bp.register_blueprint(task_bp, url_prefix="/tasks")
api_bp.register_blueprint(auth_bp, url_prefix="/auth")