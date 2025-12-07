from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config
from datetime import datetime


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # ✅ Log DB URI so we can see it in Render logs
    print("DB URI at startup:", app.config["SQLALCHEMY_DATABASE_URI"], flush=True)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    @app.context_processor
    def inject_now():
        return {"now": datetime.utcnow}

    # Ensure models are imported and tables exist
    with app.app_context():
        from app import models  # noqa: F401
        # ✅ This will create /tmp/taskflow.db and all tables if not present
        db.create_all()

    from app.blueprints.core.routes import core_bp
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.dashboard.routes import dashboard_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    return app