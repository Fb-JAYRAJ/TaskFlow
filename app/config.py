import os


class Config:
    # Secret key
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    # 1) Try DATABASE_URL from env (for future Postgres etc.)
    db_url = os.environ.get("DATABASE_URL")

    # 2) If not set, use SQLite in /tmp (always writable on Render)
    if not db_url:
        db_url = "sqlite:////tmp/taskflow.db"

    # 3) Fix old-style postgres:// URLs (if Render ever gives one)
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False