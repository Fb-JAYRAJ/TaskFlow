# app/blueprints/dashboard/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from datetime import datetime

from app.extensions import db
from app.models.task import Task
from app.models.project import Project
from .forms import TaskForm

dashboard_bp = Blueprint("dashboard", __name__)

# Require login for ALL dashboard pages
@dashboard_bp.before_request
@login_required
def require_login():
    pass


# ---------------------------
# DASHBOARD HOME
# ---------------------------
@dashboard_bp.route("/")
def home():
    upcoming_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.due_date >= datetime.utcnow()
    ).count()

    completed = Task.query.filter_by(
        user_id=current_user.id,
        status="completed"
    ).count()

    projects = Project.query.filter_by(
        user_id=current_user.id
    ).order_by(Project.created_at.desc()).all()

    recent_tasks = Task.query.filter_by(
        user_id=current_user.id
    ).order_by(Task.created_at.desc()).limit(5).all()

    return render_template(
        "dashboard/home.html",
        tasks_due=upcoming_tasks,
        completed=completed,
        projects=projects,
        recent_tasks=recent_tasks
    )


# ---------------------------
# TASKS PAGE
# ---------------------------
@dashboard_bp.route("/tasks")
def tasks_page():
    tasks = Task.query.filter_by(
        user_id=current_user.id
    ).order_by(Task.created_at.desc()).all()

    return render_template("dashboard/tasks.html", tasks=tasks)


# ---------------------------
# CREATE TASK
# ---------------------------
@dashboard_bp.route("/tasks/new", methods=["GET", "POST"])
def task_create():
    form = TaskForm()

    # Load only this user's projects
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.name).all()
    form.project_id.choices = [(p.id, p.name) for p in projects]

    if request.method == "POST" and form.validate_on_submit():
        task = Task(
            title=form.title.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            due_date=form.due_date.data,
            status=form.status.data,
            user_id=current_user.id,
            project_id=form.project_id.data,
            created_at=datetime.utcnow()
        )

        db.session.add(task)
        db.session.commit()
        flash("Task created successfully!", "success")
        return redirect(url_for("dashboard.tasks_page"))

    return render_template("dashboard/task_form.html", form=form, form_action="Create Task")


# ---------------------------
# EDIT TASK
# ---------------------------
@dashboard_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def task_edit(task_id):
    task = Task.query.get_or_404(task_id)

    # SECURITY: prevent editing other users' tasks
    if task.user_id != current_user.id:
        abort(403)

    form = TaskForm(obj=task)

    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.name).all()
    form.project_id.choices = [(p.id, p.name) for p in projects]

    if request.method == "POST" and form.validate_on_submit():
        task.title = form.title.data.strip()
        task.description = form.description.data.strip() if form.description.data else None
        task.due_date = form.due_date.data
        task.status = form.status.data
        task.project_id = form.project_id.data

        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for("dashboard.tasks_page"))

    return render_template("dashboard/task_form.html", form=form, form_action="Edit Task")


# ---------------------------
# DELETE TASK
# ---------------------------
@dashboard_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def task_delete(task_id):
    task = Task.query.get_or_404(task_id)

    # SECURITY: only owner can delete
    if task.user_id != current_user.id:
        abort(403)

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("dashboard.tasks_page"))


# ---------------------------
# PROJECTS PAGE
# ---------------------------
@dashboard_bp.route("/projects")
def projects_page():
    projects = Project.query.filter_by(
        user_id=current_user.id
    ).order_by(Project.created_at.desc()).all()

    return render_template("dashboard/projects.html", projects=projects)


# ---------------------------
# ANALYTICS PAGE
# ---------------------------
@dashboard_bp.route("/analytics")
def analytics_page():
    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    values = [3, 5, 2, 7, 4, 6, 3]

    completed = Task.query.filter_by(
        user_id=current_user.id,
        status="completed"
    ).count()

    pending = Task.query.filter_by(
        user_id=current_user.id,
        status="pending"
    ).count()

    projects = Project.query.filter_by(
        user_id=current_user.id
    ).all()

    return render_template(
        "dashboard/analytics.html",
        labels=labels,
        values=values,
        completed=completed,
        pending=pending,
        projects=projects
    )


# ---------------------------
# SETTINGS PAGE
# ---------------------------
@dashboard_bp.route("/settings")
def settings_page():
    return render_template("dashboard/settings.html")