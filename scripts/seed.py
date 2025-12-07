from app import create_app
from app.extensions import db
from app.models import User, Project, Task
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    # Reset database
    db.drop_all()
    db.create_all()

    # Create demo user
    user = User(
        email="demo@taskflow.com",
        password_hash="demo"
    )
    db.session.add(user)
    db.session.commit()

    # Create sample projects
    project1 = Project(name="Website Redesign", user_id=user.id)
    project2 = Project(name="Mobile App Development", user_id=user.id)

    db.session.add(project1)
    db.session.add(project2)
    db.session.commit()

    # Create sample tasks
    task1 = Task(
        title="Design homepage layout",
        user_id=user.id,
        project_id=project1.id,
        due_date=datetime.utcnow() + timedelta(days=1)
    )

    task2 = Task(
        title="Create login API",
        user_id=user.id,
        project_id=project2.id,
        due_date=datetime.utcnow() + timedelta(days=3)
    )

    task3 = Task(
        title="UI fixes in dashboard",
        user_id=user.id,
        project_id=project1.id,
        due_date=datetime.utcnow() + timedelta(days=2)
    )

    db.session.add_all([task1, task2, task3])
    db.session.commit()

    print("Dummy data inserted successfully!")