from datetime import datetime
from flask import Blueprint, request, jsonify
from models import db, User, Task
from auth import hash_password, verify_password, create_token, verify_token

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
    if not user or not verify_password(data['password'], user.password):
        return jsonify({'error': 'Invalid credentials'}), 401

    token = create_token(user.id)
    return jsonify({'token': token}), 200

# Add Task
@bp.route('/tasks', methods=['POST'])
def add_task():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Missing token'}), 401

    user_id = verify_token(token.split()[1])
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

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
        created_by=user_id
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

# Get Tasks
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Missing token'}), 401

    user_id = verify_token(token.split()[1])
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

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
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'Missing token'}), 401

    user_id = verify_token(token.split()[1])
    if not user_id:
        return jsonify({'error': 'Invalid token'}), 401

    task = Task.query.get(task_id)
    if not task or task.created_by != user_id:
        return jsonify({'error': 'Task not found or unauthorized'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200
