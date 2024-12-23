from flask_sqlalchemy import SQLAlchemy
 
db = SQLAlchemy()
 
# User model
class User(db.Model):
    id = db.Column(db.String(50), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Store plain passwords (not secure)
 
# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Enum('High', 'Medium', 'Low', name='priority_enum'), nullable=False)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)