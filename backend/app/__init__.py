# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy() # Database object
migrate = Migrate() # Migration tool
jwt = JWTManager()

def create_app():
  """Flask Application Factory"""
  app = Flask(__name__)
  app.config.from_object(Config) # Load settings from config.py

  # Initialize database and migration tool
  db.init_app(app)
  jwt.init_app(app)
  migrate.init_app(app, db)

  # Imports models **AFTER** db is initialized
  from app import models

  # Register custom commands
  from app.cli import seed, reset_db
  app.cli.add_command(seed) # Register command
  app.cli.add_command(reset_db)

  # Register API Blueprints
  from app.api import api_bp
  app.register_blueprint(api_bp, url_prefix="/api")
  
  return app # Returns the Flask app