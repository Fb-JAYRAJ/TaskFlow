import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    db_url = os.environ.get("DATABASE_URL")

    if db_url:
        # If in future we use Postgres on Render
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = db_url
    else:
        # ✅ Always use /tmp for SQLite (works on Render & locally)
        SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/taskflow.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False