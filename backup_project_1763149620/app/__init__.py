from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Flask-Login required settings
    login_manager.login_view = "core.home"
    login_manager.login_message = None

    # Register blueprints
    from app.blueprints.core import core_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.api.v1 import api_v1_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(api_v1_bp, url_prefix="/api/v1")

    return app