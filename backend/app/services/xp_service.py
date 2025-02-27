# app/services/xp_service.py
from app import db

def xp_required_for_level(level):
  """Calculate required XP for the next level using an exponential formula"""
  return int(100 * (level ** 1.5))

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
    required_xp = xp_required_for_level(user.level) # Update next level threshold