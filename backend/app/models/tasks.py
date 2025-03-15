# app/models/tasks.py
from datetime import datetime
from app import db
import sqlalchemy as sa 

# Enum 定義(SQLAlchemy　用)
task_difficulty_enum = sa.Enum("easy", "medium", "hard", name="task_difficulty", create_type=False)
task_type_enum = sa.Enum("todo", "habit", "daily", name="task_type", create_type=False)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    difficulty = db.Column(task_difficulty_enum, nullable=False)
    type = db.Column(task_type_enum, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    # リレーションシップ
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    user = db.relationship('User', back_populates='tasks')

    def __repr__(self):
      return f'<Task {self.name} - User {self.user_id}>'