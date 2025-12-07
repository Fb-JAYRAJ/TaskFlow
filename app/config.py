import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Detect if running on Render
RUNNING_ON_RENDER = os.environ.get("RENDER") is not None


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    if RUNNING_ON_RENDER:
        # On Render: use /tmp (writable filesystem)
        db_dir = "/tmp"
        db_path = os.path.join(db_dir, "taskflow.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"
    else:
        # Local dev: use instance/taskflow.db (like before)
        db_dir = os.path.join(BASE_DIR, "..", "instance")
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "taskflow.db")
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            "DATABASE_URL",
            f"sqlite:///{db_path}",
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False