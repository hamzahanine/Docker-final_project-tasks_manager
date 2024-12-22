import secrets
from datetime import datetime, timedelta
from flask import current_app
from models import db, Token

# Generate a token for a user
def create_token(user_id):
    token_value = secrets.token_hex(16)
    new_token = Token(token=token_value, user_id=user_id, created_at=datetime.utcnow())
    db.session.add(new_token)
    db.session.commit()
    return token_value

# Verify if a token is valid
def verify_token(token):
    token_record = Token.query.filter_by(token=token).first()
    return token_record.user_id if token_record else None

# Hash password (Simple string storage)
def hash_password(password):
    return password  # Store as plain string (Not secure, for simplicity only)

# Verify password (Simple string comparison)
def verify_password(password, stored_password):
    return password == stored_password
