# app/cli.py
import click
from flask.cli import with_appcontext
from faker import Faker
from app import db
from app.models.user import User
from app.models.tasks import Task 

fake = Faker()

@click.command("seed")
@click.option("--users", default=5, help="Number of users to create")
@click.option("--tasks", default=10, help="Number of tasks to create")
@with_appcontext
def seed(users, tasks):
  """Create ramdom users and tasks."""
  print(f"🌱 Seeding {users} users and {tasks} tasks...")

  # 1️⃣ Create Users
  user_list = []
  for _ in range(users):
    user = User(username=fake.user_name(), email=fake.email())
    user.set_password(fake.password())
    db.session.add(user)
    user_list.append(user)

  db.session.commit() # Save users first so we can reference them for tasks
  print(f"✅ Created {users} users.")

  # 2️⃣ Create Tasks
  for _ in range(tasks):
    user = fake.random.choice(user_list)  # Randomly assign task to a user
    task = Task(name=fake.sentence(nb_words=4), user_id=user.id, completed=fake.boolean())
    db.session.add(task)

  db.session.commit()
    
  print(f"✅ Created {tasks} tasks.")
  print("🎉 Database seeded successfully!")

@click.command("reset-db")
@with_appcontext
def reset_db():
  """Delete and recreate all databases tables."""
  db.drop_all()
  db.create_all()
  print("Database reset successfully!")