from app import db
from app.models.tasks import Task

def reset_daily_tasks():
  """Reset daily tasks at midnight."""
  tasks = Task.query.filter_by(type="daily").all()

  for task in tasks:
    task.completed = False

  db.session.commit()