from app.extensions import db
from datetime import datetime

class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # FK → User
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"<Activity {self.message}>"