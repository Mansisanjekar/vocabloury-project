"""
Database management for VocabLoury application
"""

import sqlite3
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from config.settings import DATABASE_NAME


class DatabaseManager:
    def __init__(self):
        # Always use the directory where the script is located
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.db_file = os.path.join(base_dir, DATABASE_NAME)
        self.initialize_database()
    
    def initialize_database(self):
        """Create the database and tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create accounts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    profession TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create auth_tokens table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auth_tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    token TEXT NOT NULL,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES accounts (id)
                )
            ''')

            # Create word_history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS word_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    word TEXT NOT NULL,
                    meaning TEXT,
                    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    
    def hash_password(self, password, salt=None):
        """Hash password with salt"""
        if salt is None:
            salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        return password_hash, salt
    
    def word_history(self, username, word, meaning):
        """Add a word to the history"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO word_history (username, word, meaning)
                VALUES (?, ?, ?)
            ''', (username, word, meaning))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def create_user(self, username, email, password, profession):
        """Create a new user"""
        try:
            print(f"Attempting to create user: {username}, {email}, {profession}")
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Hash password with salt
            password_hash, salt = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO accounts (username, email, password, salt, profession)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, salt, profession))
            
            conn.commit()
            print("User created successfully!")
            return True, "User created successfully!"
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")
            if "username" in str(e):
                return False, "Username already exists!"
            elif "email" in str(e):
                return False, "Email already exists!"
            return False, "An error occurred!"
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False, f"Database error: {e}"
        finally:
            conn.close()
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, password, salt FROM accounts WHERE username = ?', 
                          (username,))
            result = cursor.fetchone()
            
            if result:
                user_id, stored_hash, salt = result
                # Hash the provided password with stored salt
                password_hash, _ = self.hash_password(password, salt)
                
                # Compare hashes
                if password_hash == stored_hash:
                    return True, user_id
            return False, None
        except sqlite3.Error as e:
            return False, None
        finally:
            conn.close()
    
    def create_remember_token(self, user_id):
        """Create a remember me token for the user"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Generate a secure token
            token = secrets.token_hex(32)
            # Token expires in 30 days
            expires_at = datetime.now() + timedelta(days=30)
            
            # Delete any existing tokens for this user
            cursor.execute('DELETE FROM auth_tokens WHERE user_id = ?', (user_id,))
            
            # Insert new token
            cursor.execute('''
                INSERT INTO auth_tokens (user_id, token, expires_at)
                VALUES (?, ?, ?)
            ''', (user_id, token, expires_at))
            
            conn.commit()
            return token
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
    
    def verify_remember_token(self, token):
        """Verify a remember me token"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Get token info
            cursor.execute('''
                SELECT a.id, a.username, t.expires_at 
                FROM auth_tokens t
                JOIN accounts a ON t.user_id = a.id
                WHERE t.token = ? AND t.expires_at > ?
            ''', (token, datetime.now()))
            
            result = cursor.fetchone()
            
            if result:
                user_id, username, expires_at = result
                return True, username
            return False, None
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False, None
        finally:
            conn.close()
    
    def delete_remember_token(self, token):
        """Delete a remember me token"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM auth_tokens WHERE token = ?', (token,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()
    
    def get_profession(self, username):
        """Get user's profession"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT profession FROM accounts WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            conn.close()
