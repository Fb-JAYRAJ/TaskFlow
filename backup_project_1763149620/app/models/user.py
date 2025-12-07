from app.extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    projects = db.relationship("Project", backref="owner", lazy=True)
    tasks = db.relationship("Task", backref="assignee", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"