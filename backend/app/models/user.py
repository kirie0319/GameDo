# app/models/user.py
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    gold = db.Column(db.Integer, default=0)
    hp = db.Column(db.Integer, default=100)

    # リレーションシップ
    tasks = db.relationship('Task', back_populates='user', cascade='all, delete', passive_deletes=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # This section converts User class into JSON format
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'xp': self.xp,
            'level': self.level,
            'gold': self.gold,
            'hp': self.hp,
            'task': [task.name for task in self.tasks]
        }

    # for debugging
    def __repr__(self):
        return f'<User {self.username}>'