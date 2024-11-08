import random
import string
import re

def generate_password(length=12, use_upper=True, use_numbers=True, use_special=True):
    """Generate a secure password with customizable options."""
    characters = string.ascii_lowercase
    if use_upper:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def validate_password(password, min_length=8, require_upper=True, require_numbers=True, require_special=True):
    """Validate password based on security criteria."""
    if len(password) < min_length:
        return False, "Password is too short"

    if require_upper and not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"

    if require_numbers and not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number"

    if require_special and not any(char in string.punctuation for char in password):
        return False, "Password must contain at least one special character"

    return True, "Password is valid"

def check_password_strength(password):
    """Return a strength rating for the password: Weak, Medium, or Strong."""
    length_score = len(password) >= 12
    upper_score = any(char.isupper() for char in password)
    number_score = any(char.isdigit() for char in password)
    special_score = any(char in string.punctuation for char in password)

    score = sum([length_score, upper_score, number_score, special_score])

    if score == 4:
        return "Strong"
    elif score == 3:
        return "Medium"
    else:
        return "Weak"
