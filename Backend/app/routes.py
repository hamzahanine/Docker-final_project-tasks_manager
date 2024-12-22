from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, User, Task
import base64
 
bp = Blueprint('routes', __name__)
 
@bp.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Task Management API!'}), 200
 
# Helper function to extract and validate Basic Auth credentials
def get_authenticated_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Basic "):
        return None
 
    try:
        auth_type, auth_credentials = auth_header.split(" ")
        user_id, password = base64.b64decode(auth_credentials).decode("utf-8").split(":")
        user = User.query.get(user_id)
        if user and user.password == password:
            return user
    except Exception as e:
        return None
    return None
 
# User Registration
@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.get(data['id']):
        return jsonify({'error': 'User ID already exists'}), 400
 
    # Directly store the plain password (NOT SECURE, for testing purposes only)
    new_user = User(id=data['id'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201
 
# User Login
@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.get(data['id'])
 
    # Check if user exists and password matches
    if user and data['password'] == user.password:
        return jsonify({'message': 'Login successful!', 'user_id': user.id}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
 
# Add Task
@bp.route('/tasks', methods=['POST'])
def add_task():
    user = get_authenticated_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
 
    data = request.json
 
    # Convert due_date string to a datetime.date object
    try:
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
 
    new_task = Task(
        title=data['title'],
        description=data['description'],
        due_date=due_date,
        priority=data['priority'],
        created_by=user.id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201
 
# Get Tasks
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    user = get_authenticated_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
 
    tasks = Task.query.filter_by(created_by=user.id).all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.strftime('%Y-%m-%d'),
        'priority': task.priority
    } for task in tasks]), 200
 
# Delete Task
@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    user = get_authenticated_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
 
    task = Task.query.get(task_id)
    if not task or task.created_by != user.id:
        return jsonify({'error': 'Task not found or unauthorized'}), 404
 
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200