# seeds/seed_users.py
from app import create_app, db
from app.models.user import User

def seed_data():
  """Create test users."""
  app = create_app()
  with app.app_context():

    # 1️⃣ Create Users
    user1 = User(username="JohnDoe", email="john@example.com")
    user1.set_password("password123")  # Securely store password

    user2 = User(username="JaneDoe", email="jane@example.com")
    user2.set_password("password456")

    db.session.add_all([user1, user2])
    db.session.commit()  # Save users first so we can reference their IDs

    print(f"✅ Seeded users: {user1.username}, {user2.username}")

if __name__ == "__main__":
  seed_data()