import secrets
from datetime import datetime
from models import db, Token
from werkzeug.security import generate_password_hash, check_password_hash

# Generate a token for a user
def create_token(user_id):
    token_value = secrets.token_hex(16)  # Generate a secure random token
    new_token = Token(
        token=token_value,
        user_id=user_id,
        created_at=datetime.utcnow()
    )
    db.session.add(new_token)
    db.session.commit()
    return token_value

# Verify if a token is valid
def verify_token(token):
    token_record = Token.query.filter_by(token=token).first()
    return token_record.user_id if token_record else None  # Return user_id if token exists

# Hash password securely
def hash_password(password):
    return generate_password_hash(password)  # Use hashing for secure password storage

# Verify password securely
def verify_password(password, stored_password):
    return check_password_hash(stored_password, password)  # Compare hashed password securely
