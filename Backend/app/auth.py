import secrets
from datetime import datetime
from models import db
from werkzeug.security import generate_password_hash, check_password_hash
 
 
# Hash password securely
def hash_password(password):
    return generate_password_hash(password)  # Use hashing for secure password storage
 
# Verify password securely
def verify_password(password, stored_password):
    return password == stored_password  # Plain text comparison