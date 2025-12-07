from flask import Blueprint, redirect, url_for, render_template

core_bp = Blueprint("core", __name__)

@core_bp.route("/")
def home():
    # send root traffic to the dashboard route instead of rendering base.html directly
    return redirect(url_for("dashboard.home"))