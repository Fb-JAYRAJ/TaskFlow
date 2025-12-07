# app/blueprints/core/routes.py
from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

core_bp = Blueprint("core", __name__)

@core_bp.route("/")
def index():
    # If logged in → skip landing page, go to dashboard
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.home"))

    # If not logged in → show landing page
    return render_template("core/index.html")