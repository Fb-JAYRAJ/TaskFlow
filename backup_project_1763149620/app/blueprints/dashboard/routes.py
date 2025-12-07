from flask import Blueprint, render_template
from app.models.task import Task
from app.models.project import Project
from datetime import datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def home():
    user_id = 1  # demo user

    upcoming_tasks = Task.query.count()
    completed = Task.query.filter_by(status="completed").count()
    projects = Project.query.all()
    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()

    return render_template(
        "dashboard/home.html",
        tasks_due=upcoming_tasks,
        completed=completed,
        projects=projects,
        recent_tasks=recent_tasks
    )