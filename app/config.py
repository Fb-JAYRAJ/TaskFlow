import os

# Base directory of the app package (…/src/app)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Instance directory (…/src/instance)
INSTANCE_DIR = os.path.join(BASE_DIR, "..", "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)  # ✅ Make sure it exists (local + Render)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    # Use DATABASE_URL if provided (for future Postgres), otherwise local SQLite in /instance
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(INSTANCE_DIR, "taskflow.db")
    )

    # Fix old-style Postgres URLs if Render gives one later
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False