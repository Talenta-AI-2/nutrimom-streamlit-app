import re


def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit")
    if not any(char.isupper() for char in password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise ValueError("Password must contain at least one lowercase letter")
    if ' ' in password:
        raise ValueError("Password must not contain spaces")
    return True


def validate_username(username):
    if not re.match("^[a-zA-Z0-9_.-]+$", username):
        raise ValueError("Username can only contain letters, numbers, underscores, periods, and hyphens")
    if not (3 <= len(username) <= 30):
        raise ValueError("Username must be between 3 and 30 characters long")
    return True
