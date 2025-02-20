# seeds/seed_tasks.py
from app import create_app, db
from app.models.tasks import Task

def seed_data():
  """Create test tasks."""
  app = create_app()
  with app.app_context():

    # 2️⃣ Create Tasks for Users
    task1 = Task(name="Buy groceries", user_id=user1.id)
    task2 = Task(name="Go to the gym", user_id=user1.id)
    task3 = Task(name="Finish homework", user_id=user2.id)

    db.session.add_all([task1, task2, task3])
    db.session.commit()

    print(f"✅ Seeded tasks: {task1.name}, {task2.name}, {task3.name}")

if __name__ == "__main__":
  seed_data()
