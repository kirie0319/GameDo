# app/services/xp_service.py
from datetime import datetime
from app import db
from app.models.user import User
from app.models.tasks import Task


# XP Scaling (Adjustable)
DIFFICULTY_MULTIPLIER = {
  "easy": 1.0,
  "medium": 1.5,
  "hard": 2.0
}

# HP Penalty based on task difficulty
HP_PENALTY = {
  "easy": 2,
  "medium": 4,
  "hard": 6
}

# Base XP Formula
def xp_required_for_level(level):
  """Calculate required XP for the next level using an exponential formula"""
  return int(100 * (level ** 1.5))

def calculate_xp(task_difficulty, streak):
  """Calculate XP based on task difficulty and streak multiplier"""
  base_xp = 10 # Base XP per task
  multiplier = DIFFICULTY_MULTIPLIER.get(task_difficulty, 1.0)
  streak_bonus = 1.0 + (streak * 0.05) # 5% bonus per streak
  return int(base_xp * multiplier * streak_bonus)

def update_streak(task):
  """Update streak if the task was completed on consecutive days."""
  today = datetime.utcnow().date()

  if task.last_completed_at:
    last_completed_at = task.last_completed_at.date()
    if (today - last_completed_at).days == 1:
      task.streak_count += 1 # Increase streak
    else:
      task.streak_count = 1 # Reset streak
  else:
    task.streak_count = 1 # First completion

  task.last_completed_at = datetime.utcnow()
  db.session.commit()

def apply_hp_penalty():
  """Reduce HP for users who miss daily tasks."""
  users = User.query.all()
  today = datetime.utcnow().date()

  for user in users:
    daily_tasks = Task.query.filter_by(user_id=user.id, type="daily").all()

    for task in daily_tasks:
      if not task.completed and task.last_completed_at:
        last_date = task.last_completed_at.date()
        if (today - last_date).days >= 1: # Missed a day
          Penalty = HP_PENALTY.get(task.difficulty, 2) # Default -2 HP
          user.hp -= penalty 

          # Check if the user "dies"
          if user.hp <= 0:
            handle_death(user)
  db.session.commit()

def handle_death(user):
  """Reset XP, Gold, and Streks when HP reaches 0."""
  user.hp = 50 # Reset HP to half
  user.xp = 0
  user.gold = 0

  # Reset streaks
  tasks = Task.query.filter_by(user_id=user.id).all()
  for task in tasks:
    task.streak_count = 0

  db.session.commit()

def add_xp(user, task_xp):
  """Add XP to a user and check if they level up."""
  user.xp += task_xp # Increase XP
  check_level_up(user) # Check for level up
  db.session.commit()

def check_level_up(user):
  """Check if the user has enough XP to level up."""
  required_xp = xp_required_for_level(user.level)

  while user.xp >= required_xp: # If XP exceeds level requirement
    user.level += 1 # Increase Level
    user.xp -= required_xp # Deduct XP used for level up
    user.gold += 50 # Reward gold for leveling up
    user.hp = min(user.hp + 10, 100) # Restore HP (Max 100)
    required_xp = xp_required_for_level(user.level) # Update next level threshold

  db.session.commit()