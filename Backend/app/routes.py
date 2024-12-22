from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, User, Task
from auth import verify_password, hash_password
import base64
 
bp = Blueprint('routes', __name__)
 
@bp.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to the Task Management API!'}), 200
 
# User Registration
@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.get(data['id']):
        return jsonify({'error': 'User ID already exists'}), 400

    # Securely store hashed password
    hashed_password = hash_password(data['password'])
    new_user = User(id=data['id'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201
 
# User Login
@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.get(data['id'])

    # Securely verify password
    if user and verify_password(data['password'], user.password):
        return jsonify({'message': 'Login successful!', 'user_id': user.id}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
 
# Add Task
def get_authenticated_user():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_type, credentials = auth_header.split(' ')
        user_id, password = base64.b64decode(credentials).decode('utf-8').split(':')
        user = User.query.get(user_id)
        if user and verify_password(password, user.password):
            return user
    return None

@bp.route('/tasks', methods=['POST'])
def add_task():
    user = get_authenticated_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
 
# Get Tasks
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    if not User.query.get(user_id):
        return jsonify({'error': 'Unauthorized'}), 401
 
    tasks = Task.query.filter_by(created_by=user_id).all()
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
    user_id = request.args.get('user_id')
    if not User.query.get(user_id):
        return jsonify({'error': 'Unauthorized'}), 401
 
    task = Task.query.get(task_id)
    if not task or task.created_by != user_id:
        return jsonify({'error': 'Task not found or unauthorized'}), 404
 
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200