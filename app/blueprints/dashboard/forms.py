# app/blueprints/dashboard/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    due_date = DateField("Due date (YYYY-MM-DD)", format="%Y-%m-%d", validators=[Optional()])
    status = SelectField("Status", choices=[("todo", "To do"), ("in_progress", "In progress"), ("completed", "Completed")], default="todo")
    project_id = SelectField("Project", coerce=int, validators=[Optional()])
    submit = SubmitField("Save")