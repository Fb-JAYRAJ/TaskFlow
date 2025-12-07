# app/__init__.py
from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config
from datetime import datetime

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    # -------------------------
    # Context processors
    # -------------------------
    # Provide `now()` to templates so {{ now().year }} works.
    @app.context_processor
    def inject_now():
        # Option A: a callable, use in template as {{ now().year }}
        return {"now": datetime.utcnow}
        # Option B: if you prefer a single value, replace the above with:
        # return {"current_year": datetime.utcnow().year}

    # Ensure models package is imported so Alembic / Flask-Migrate sees metadata.
    # This is done inside an app context to avoid import-time DB access issues.
    with app.app_context():
        # Importing the models package triggers model declarations.
        # app/models/__init__.py should import all model modules.
        from app import models  # noqa: F401

    # -------------------------
    # Register blueprints
    # -------------------------
    from app.blueprints.core.routes import core_bp
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.dashboard.routes import dashboard_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")

    return app