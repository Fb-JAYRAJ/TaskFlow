# app/config.py
import os
from pathlib import Path

# /src/app
BASE_DIR = Path(__file__).resolve().parent

# Default local DB path: /src/instance/taskflow.db
default_db_path = BASE_DIR.parent / "instance" / "taskflow.db"

# On Render we’ll store the sqlite file in /tmp (always writable there)
# We'll signal that with an env var RENDER=1 on Render
if os.environ.get("RENDER") == "1":
    default_db_path = Path("/tmp") / "taskflow.db"

# Make sure the folder exists
default_db_path.parent.mkdir(parents=True, exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    # Use DATABASE_URL (for future Postgres) or fallback to sqlite file
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{default_db_path}",
    )

    # Render sometimes gives old-style postgres:// URLs
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False