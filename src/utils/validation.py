"""
Form validation utilities for VocabLoury application
"""

import re


class FormValidator:
    """Form validation utilities"""
    
    @staticmethod
    def validate_username(username):
        """Validate username"""
        if not username or len(username.strip()) == 0:
            return False, "Username is required"
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 20:
            return False, "Username must be less than 20 characters"
        if not username.replace('_', '').replace('-', '').isalnum():
            return False, "Username can only contain letters, numbers, _ and -"
        return True, ""
    
    @staticmethod
    def validate_email(email):
        """Validate email"""
        if not email or len(email.strip()) == 0:
            return False, "Email is required"
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Please enter a valid email address"
        return True, ""
    
    @staticmethod
    def validate_password(password):
        """Validate password"""
        if not password or len(password) == 0:
            return False, "Password is required"
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if len(password) > 50:
            return False, "Password must be less than 50 characters"
        return True, ""
    
    @staticmethod
    def validate_password_match(password, confirm_password):
        """Validate password confirmation"""
        if password != confirm_password:
            return False, "Passwords do not match"
        return True, ""
    
    @staticmethod
    def validate_profession(profession):
        """Validate profession selection"""
        if not profession or profession == "":
            return False, "Please select a profession"
        return True, ""
