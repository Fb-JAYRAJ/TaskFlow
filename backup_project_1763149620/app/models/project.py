from app.extensions import db
from datetime import datetime

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FK → User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # relationship
    tasks = db.relationship("Task", backref="project", lazy=True)

    def __repr__(self):
        return f"<Project {self.name}>"