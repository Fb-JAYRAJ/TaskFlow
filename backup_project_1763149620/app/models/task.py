from app.extensions import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    status = db.Column(db.String(50), default="pending")
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FK → User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # FK → Project
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"