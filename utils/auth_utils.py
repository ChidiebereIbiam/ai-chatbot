import bcrypt
from .db_utils import add_user, get_user_password

def hash_password(password):
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(input_password, hashed_password):
    """Verify a password against its hash."""
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

def register_user(name, email, phone, username, password):
    """Register a new user with hashed password."""
    hashed_pw = hash_password(password)
    return add_user(name, email, phone, username, hashed_pw)

def authenticate_user(username, password):
    """Authenticate a user by username and password."""
    hashed_password = get_user_password(username)
    if hashed_password and verify_password(password, hashed_password):
        return True
    return False
