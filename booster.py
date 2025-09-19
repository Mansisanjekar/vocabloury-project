import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
from PIL import Image, ImageTk
import re
import json
import os
import hashlib
import secrets
from datetime import datetime, timedelta
from plyer import notification
import threading
import time
import webbrowser
import requests
from functools import partial

# Windows-specific imports - will be handled conditionally
try:
from win10toast import ToastNotifier
from winotify import Notification, audio
    WINDOWS_NOTIFICATIONS = True
except ImportError:
    WINDOWS_NOTIFICATIONS = False

import sys
import argparse
import random
import string
from typing import Dict, List, Optional
import math

# Global theme variables
THEME_MODE = "dark"
ctk.set_appearance_mode(THEME_MODE)
ctk.set_default_color_theme("blue")

# Color schemes
COLORS = {
    "dark": {
        "bg": "#1a1a1a",
        "secondary_bg": "#2b2b2b",
        "accent": "#1f538d",
        "text": "#ffffff",
        "text_secondary": "#cccccc",
        "border": "#444444"
    },
    "light": {
        "bg": "#ffffff",
        "secondary_bg": "#f0f0f0",
        "accent": "#0078d4",
        "text": "#000000",
        "text_secondary": "#666666",
        "border": "#cccccc"
    }
}

class AnimatedBackground(ctk.CTkFrame):
    """Animated background with floating particles"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.particles = []
        self.animation_running = True
        self.create_particles()
        self.animate()
    
    def create_particles(self):
        """Create floating particles"""
        for _ in range(20):
            particle = {
                'x': random.randint(0, 1200),
                'y': random.randint(0, 800),
                'size': random.randint(2, 6),
                'speed_x': random.uniform(-1, 1),
                'speed_y': random.uniform(-1, 1),
                'opacity': random.uniform(0.3, 0.8)
            }
            self.particles.append(particle)
    
    def animate(self):
        """Animate particles"""
        if not self.animation_running:
            return
            
        # Update particle positions
        for particle in self.particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Bounce off edges
            if particle['x'] <= 0 or particle['x'] >= 1200:
                particle['speed_x'] *= -1
            if particle['y'] <= 0 or particle['y'] >= 800:
                particle['speed_y'] *= -1
            
            # Keep particles in bounds
            particle['x'] = max(0, min(1200, particle['x']))
            particle['y'] = max(0, min(800, particle['y']))
        
        # Schedule next animation frame
        self.after(50, self.animate)

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

class AnimatedButton(ctk.CTkButton):
    """Button with hover animations"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.original_fg_color = kwargs.get('fg_color', ["#3B8ED0", "#1F6AA5"])
        self.original_hover_color = kwargs.get('hover_color', ["#36719F", "#144870"])
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event):
        """Animation on mouse enter"""
        self.configure(fg_color=self.original_hover_color)
    
    def on_leave(self, event):
        """Animation on mouse leave"""
        self.configure(fg_color=self.original_fg_color)

profession_to_topic = {
    "Student": "education",
    "Entrepreneur": "money",
    "Scientist": "science",
    "Musician": "music",
    "Writer": "writing"
}

class DatabaseManager:
    def __init__(self):
        # Always use the directory where booster.py is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(base_dir, "authentication.db")
        self.initialize_database()
    
    def initialize_database(self):
        """Create the database and tables if they don't exist"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Rename users table to accounts
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
            
            # Rename remember_tokens table to auth_tokens
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auth_tokens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    token TEXT NOT NULL,
                    expires_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES accounts (id)
                )
            ''')

            # Create words table with meaning column
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
    
    def word_history(self,username,word,meaning):
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
            
            # Update table name to accounts
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
            
            # Update table name to accounts
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


class AuthenticationApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("VocabLoury - Dictionary & Learning App")
        self.window.geometry("1400x800")
        self.window.resizable(True, True)
        
        # Add window close handler
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.container = ctk.CTkFrame(self.window, fg_color="transparent")
        self.container.pack(fill="both", expand=True)
        
        self.current_page = None
        self.show_login_page()
    
    def on_closing(self):
        # Stop any active notifications
        if hasattr(self.current_page, 'notification_active'):
            self.current_page.notification_active = False
            if hasattr(self.current_page, 'notification_thread'):
                if self.current_page.notification_thread:
                    self.current_page.notification_thread.join(timeout=1)
        self.window.destroy()
    
    def show_login_page(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = LoginPage(self.container, self.show_signup_page)
        self.window.title("Login - Modern Authentication")
        
    def show_signup_page(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = SignupPage(self.container, self.show_login_page)
        
    def run(self):
        self.window.mainloop()

class LoginPage(ctk.CTkFrame):
    def save_remember_token(self, token):
        """Save remember me token to a file"""
        try:
            with open('remember.token', 'w') as f:
                f.write(token)
        except Exception as e:
            print(f"Error saving token: {e}")
    
    def load_remember_token(self):
        """Load remember me token from file"""
        try:
            if os.path.exists('remember.token'):
                with open('remember.token', 'r') as f:
                    return f.read().strip()
        except Exception as e:
            print(f"Error loading token: {e}")
        return None
    
    def delete_remember_token(self):
        """Delete the remember me token file"""
        try:
            if os.path.exists('remember.token'):
                os.remove('remember.token')
        except Exception as e:
            print(f"Error deleting token: {e}")
    
    def __init__(self, parent, show_signup_callback):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.show_signup_callback = show_signup_callback  # Store the callback
        self.validator = FormValidator()
        
        # Check for remember me token
        token = self.load_remember_token()
        if token:
            db = DatabaseManager()
            success, username = db.verify_remember_token(token)
            if success:
                self.destroy()
                WelcomePage(self.master, username)
                return
            else:
                self.delete_remember_token()
        
        # Create animated background
        self.animated_bg = AnimatedBackground(self, fg_color="transparent")
        self.animated_bg.pack(fill="both", expand=True)
        
        # Create two frames for split screen
        left_frame = ctk.CTkFrame(self.animated_bg, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=0)
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = ctk.CTkFrame(self.animated_bg, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=0)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Left side - Login Form
        form_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        form_frame.pack(pady=20, padx=40, expand=True)
        
        # Title
        title = ctk.CTkLabel(form_frame, text="Welcome Back!", 
                           font=("Helvetica", 32, "bold"))
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(form_frame, text="Login to your account", 
                             font=("Helvetica", 14))
        subtitle.pack(pady=(0, 20))
        
        # Username
        self.username = ctk.CTkEntry(form_frame, placeholder_text="Username *",
                                   height=45, corner_radius=10, width=300,
                                   font=("Helvetica", 14))
        self.username.pack(pady=10)
        self.username.bind("<FocusOut>", self.validate_username_field)
        
        # Username error label
        self.username_error = ctk.CTkLabel(form_frame, text="", 
                                         text_color="#FF5252", font=("Helvetica", 12))
        self.username_error.pack(pady=(0, 5))
        
        # Password
        self.password = ctk.CTkEntry(form_frame, placeholder_text="Password *",
                                   height=45, corner_radius=10, width=300, show="•",
                                   font=("Helvetica", 14))
        self.password.pack(pady=10)
        self.password.bind("<FocusOut>", self.validate_password_field)
        
        # Password error label
        self.password_error = ctk.CTkLabel(form_frame, text="", 
                                         text_color="#FF5252", font=("Helvetica", 12))
        self.password_error.pack(pady=(0, 5))
        
        # Remember me checkbox
        self.remember = ctk.CTkCheckBox(form_frame, text="Remember me",
                                      font=("Helvetica", 12))
        self.remember.pack(pady=10)
        
        # Login button with animation
        login_button = AnimatedButton(form_frame, text="🔐 Login", height=45,
                                   corner_radius=10, width=300,
                                    command=self.login,
                                    font=("Helvetica", 16, "bold"),
                                    fg_color=COLORS[THEME_MODE]["accent"],
                                    hover_color=self.darken_color(COLORS[THEME_MODE]["accent"]))
        login_button.pack(pady=20)
        
        # Signup link
        signup_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_frame.pack(pady=10)
        
        signup_label = ctk.CTkLabel(signup_frame, text="Don't have an account?",
                                  font=("Helvetica", 12))
        signup_label.pack(side="left", padx=5)
        
        signup_button = AnimatedButton(signup_frame, text="Sign Up",
                                    command=show_signup_callback,
                                     fg_color="transparent", 
                                     hover_color=COLORS[THEME_MODE]["accent"],
                                     width=100,
                                     font=("Helvetica", 12, "bold"))
        signup_button.pack(side="left")
        
        # Right side - Image
        try:
            image = Image.open("login_image.png")  # Replace with your image path
            image = image.resize((500, 600))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(right_frame, image=photo, bg="#2b2b2b")
            image_label.image = photo
            image_label.pack(expand=True)
        except:
            # Fallback text if image is not found
            ctk.CTkLabel(right_frame, text="Welcome Back!\nTo Our Community",
                        font=("Helvetica", 24, "bold"),
                        text_color="#ffffff").pack(expand=True)
    
    def validate_username_field(self, event=None):
        """Validate username field"""
        username = self.username.get()
        is_valid, error_msg = self.validator.validate_username(username)
        
        if not is_valid and username:  # Only show error if field has content
            self.username_error.configure(text=error_msg)
            self.username.configure(border_color="#FF5252")
        else:
            self.username_error.configure(text="")
            self.username.configure(border_color=COLORS[THEME_MODE]["border"])
    
    def validate_password_field(self, event=None):
        """Validate password field"""
        password = self.password.get()
        is_valid, error_msg = self.validator.validate_password(password)
        
        if not is_valid and password:  # Only show error if field has content
            self.password_error.configure(text=error_msg)
            self.password.configure(border_color="#FF5252")
        else:
            self.password_error.configure(text="")
            self.password.configure(border_color=COLORS[THEME_MODE]["border"])
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#1f538d": "#1a4a7a",
            "#0078d4": "#005a9e"
        }
        return color_map.get(color, color)
    
    def login(self):
        username = self.username.get()
        password = self.password.get()
        
        # Validate fields
        username_valid, username_error = self.validator.validate_username(username)
        password_valid, password_error = self.validator.validate_password(password)
        
        if not username_valid:
            self.username_error.configure(text=username_error)
            self.username.configure(border_color="#FF5252")
            return
        
        if not password_valid:
            self.password_error.configure(text=password_error)
            self.password.configure(border_color="#FF5252")
            return
        
        # Clear any previous errors
        self.username_error.configure(text="")
        self.password_error.configure(text="")
        self.username.configure(border_color=COLORS[THEME_MODE]["border"])
        self.password.configure(border_color=COLORS[THEME_MODE]["border"])
        
        db = DatabaseManager()
        success, user_id = db.verify_user(username, password)
        
        if success:
            # Handle remember me
            if self.remember.get():
                token = db.create_remember_token(user_id)
                if token:
                    self.save_remember_token(token)
            
            self.destroy()
            WelcomePage(self.master, username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

class SignupPage(ctk.CTkFrame):
    def __init__(self, parent, show_login_callback):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.show_login_callback = show_login_callback  # Store the callback
        self.validator = FormValidator()
        
        # Create animated background
        self.animated_bg = AnimatedBackground(self, fg_color="transparent")
        self.animated_bg.pack(fill="both", expand=True)
        
        # Create two frames for split screen
        left_frame = ctk.CTkFrame(self.animated_bg, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=0)
        left_frame.pack(side="left", fill="both", expand=True)
        
        right_frame = ctk.CTkFrame(self.animated_bg, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=0)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Left side - Signup Form
        form_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        form_frame.pack(pady=20, padx=40, expand=True)
        
        # Title
        title = ctk.CTkLabel(form_frame, text="Create Account", 
                           font=("Helvetica", 32, "bold"))
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(form_frame, text="Sign up to get started", 
                             font=("Helvetica", 14))
        subtitle.pack(pady=(0, 20))
        
        # Username
        self.username = ctk.CTkEntry(form_frame, placeholder_text="Username *",
                                   height=45, corner_radius=10, width=300,
                                   font=("Helvetica", 14))
        self.username.pack(pady=10)
        self.username.bind("<FocusOut>", self.validate_username_field)
        
        # Username error label
        self.username_error = ctk.CTkLabel(form_frame, text="", 
                                         text_color="#FF5252", font=("Helvetica", 12))
        self.username_error.pack(pady=(0, 5))
        
        # Email
        self.email = ctk.CTkEntry(form_frame, placeholder_text="Email *",
                                height=45, corner_radius=10, width=300,
                                font=("Helvetica", 14))
        self.email.pack(pady=10)
        self.email.bind("<FocusOut>", self.validate_email_field)
        
        # Email error label
        self.email_error = ctk.CTkLabel(form_frame, text="", 
                                      text_color="#FF5252", font=("Helvetica", 12))
        self.email_error.pack(pady=(0, 5))
        
        # Profession dropdown
        ctk.CTkLabel(form_frame, text="Select Profession *:", 
                    font=("Helvetica", 12)).pack(pady=(10, 0))
        self.profession_var = tk.StringVar()
        self.profession_dropdown = ctk.CTkComboBox(
            form_frame,
            values=["", "Student", "Entrepreneur", "Scientist", "Musician", "Writer"],
            variable=self.profession_var,
            width=300,
            font=("Helvetica", 14)
        )
        self.profession_dropdown.pack(pady=10)
        self.profession_dropdown.bind("<<ComboboxSelected>>", self.validate_profession_field)
        
        # Profession error label
        self.profession_error = ctk.CTkLabel(form_frame, text="", 
                                           text_color="#FF5252", font=("Helvetica", 12))
        self.profession_error.pack(pady=(0, 5))
        
        # Password
        self.password = ctk.CTkEntry(form_frame, placeholder_text="Password *",
                                   height=45, corner_radius=10, width=300, show="•",
                                   font=("Helvetica", 14))
        self.password.pack(pady=10)
        self.password.bind("<FocusOut>", self.validate_password_field)
        
        # Password error label
        self.password_error = ctk.CTkLabel(form_frame, text="", 
                                         text_color="#FF5252", font=("Helvetica", 12))
        self.password_error.pack(pady=(0, 5))
        
        # Confirm Password
        self.confirm_password = ctk.CTkEntry(form_frame, placeholder_text="Confirm Password *",
                                          height=45, corner_radius=10, width=300, show="•",
                                          font=("Helvetica", 14))
        self.confirm_password.pack(pady=10)
        self.confirm_password.bind("<FocusOut>", self.validate_confirm_password_field)
        
        # Confirm password error label
        self.confirm_password_error = ctk.CTkLabel(form_frame, text="", 
                                                 text_color="#FF5252", font=("Helvetica", 12))
        self.confirm_password_error.pack(pady=(0, 5))
        
        # Sign up button with animation
        signup_button = AnimatedButton(form_frame, text="🚀 Sign Up", height=45,
                                    corner_radius=10, width=300,
                                     command=self.signup,
                                     font=("Helvetica", 16, "bold"),
                                     fg_color=COLORS[THEME_MODE]["accent"],
                                     hover_color=self.darken_color(COLORS[THEME_MODE]["accent"]))
        signup_button.pack(pady=20)
        
        # Login link
        login_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        login_frame.pack(pady=10)
        
        login_label = ctk.CTkLabel(login_frame, text="Already have an account?",
                                 font=("Helvetica", 12))
        login_label.pack(side="left", padx=5)
        
        login_button = AnimatedButton(login_frame, text="Login",
                                   command=show_login_callback,
                                    fg_color="transparent", 
                                    hover_color=COLORS[THEME_MODE]["accent"],
                                    width=100,
                                    font=("Helvetica", 12, "bold"))
        login_button.pack(side="left")
        
        # Right side - Image
        # Load and display image
        try:
            image = Image.open("signup_image.png")  # Replace with your image path
            image = image.resize((500, 600))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(right_frame, image=photo, bg="#2b2b2b")
            image_label.image = photo
            image_label.pack(expand=True)
        except:
            # Fallback text if image is not found
            ctk.CTkLabel(right_frame, text="Join Our Community\nTo Get Started",
                        font=("Helvetica", 24, "bold"),
                        text_color="#ffffff").pack(expand=True)
        
    def validate_username_field(self, event=None):
        """Validate username field"""
        username = self.username.get()
        is_valid, error_msg = self.validator.validate_username(username)
        
        if not is_valid and username:
            self.username_error.configure(text=error_msg)
            self.username.configure(border_color="#FF5252")
        else:
            self.username_error.configure(text="")
            self.username.configure(border_color=COLORS[THEME_MODE]["border"])
    
    def validate_email_field(self, event=None):
        """Validate email field"""
        email = self.email.get()
        is_valid, error_msg = self.validator.validate_email(email)
        
        if not is_valid and email:
            self.email_error.configure(text=error_msg)
            self.email.configure(border_color="#FF5252")
        else:
            self.email_error.configure(text="")
            self.email.configure(border_color=COLORS[THEME_MODE]["border"])
    
    def validate_profession_field(self, event=None):
        """Validate profession field"""
        profession = self.profession_var.get()
        is_valid, error_msg = self.validator.validate_profession(profession)
        
        if not is_valid and profession:
            self.profession_error.configure(text=error_msg)
        else:
            self.profession_error.configure(text="")
    
    def validate_password_field(self, event=None):
        """Validate password field"""
        password = self.password.get()
        is_valid, error_msg = self.validator.validate_password(password)
        
        if not is_valid and password:
            self.password_error.configure(text=error_msg)
            self.password.configure(border_color="#FF5252")
        else:
            self.password_error.configure(text="")
            self.password.configure(border_color=COLORS[THEME_MODE]["border"])
    
    def validate_confirm_password_field(self, event=None):
        """Validate confirm password field"""
        password = self.password.get()
        confirm_password = self.confirm_password.get()
        is_valid, error_msg = self.validator.validate_password_match(password, confirm_password)
        
        if not is_valid and confirm_password:
            self.confirm_password_error.configure(text=error_msg)
            self.confirm_password.configure(border_color="#FF5252")
        else:
            self.confirm_password_error.configure(text="")
            self.confirm_password.configure(border_color=COLORS[THEME_MODE]["border"])
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#1f538d": "#1a4a7a",
            "#0078d4": "#005a9e"
        }
        return color_map.get(color, color)
        
    def signup(self):
        username = self.username.get()
        email = self.email.get()
        password = self.password.get()
        confirm_password = self.confirm_password.get()
        profession = self.profession_var.get()
        
        # Validate all fields
        username_valid, username_error = self.validator.validate_username(username)
        email_valid, email_error = self.validator.validate_email(email)
        profession_valid, profession_error = self.validator.validate_profession(profession)
        password_valid, password_error = self.validator.validate_password(password)
        password_match_valid, password_match_error = self.validator.validate_password_match(password, confirm_password)
        
        # Show validation errors
        if not username_valid:
            self.username_error.configure(text=username_error)
            self.username.configure(border_color="#FF5252")
            return
            
        if not email_valid:
            self.email_error.configure(text=email_error)
            self.email.configure(border_color="#FF5252")
            return
            
        if not profession_valid:
            self.profession_error.configure(text=profession_error)
            return
        
        if not password_valid:
            self.password_error.configure(text=password_error)
            self.password.configure(border_color="#FF5252")
            return
        
        if not password_match_valid:
            self.confirm_password_error.configure(text=password_match_error)
            self.confirm_password.configure(border_color="#FF5252")
            return
        
        # Clear all error messages
        self.clear_errors()
        
        # Create user in database
        db = DatabaseManager()
        success, message = db.create_user(username, email, password, profession)
        
        if success:
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login_callback()  # Use stored callback
        else:
            messagebox.showerror("Error", message)

    def clear_errors(self):
        """Clear all error messages and border colors"""
        self.username_error.configure(text="")
        self.email_error.configure(text="")
        self.profession_error.configure(text="")
        self.password_error.configure(text="")
        self.confirm_password_error.configure(text="")
        
        self.username.configure(border_color=COLORS[THEME_MODE]["border"])
        self.email.configure(border_color=COLORS[THEME_MODE]["border"])
        self.password.configure(border_color=COLORS[THEME_MODE]["border"])
        self.confirm_password.configure(border_color=COLORS[THEME_MODE]["border"])

class DictionaryAPI:
    """Free Dictionary API integration"""
    
    @staticmethod
    def get_word_definition(word: str) -> Optional[Dict]:
        """Get word definition from Free Dictionary API"""
        try:
            response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word.lower()}")
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return data[0]
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    @staticmethod
    def get_word_synonyms(word: str) -> List[str]:
        """Get synonyms using Datamuse API"""
        try:
            response = requests.get(f"https://api.datamuse.com/words?rel_syn={word}")
            if response.status_code == 200:
                data = response.json()
                return [item['word'] for item in data[:10]]  # Top 10 synonyms
            return []
        except Exception as e:
            print(f"Synonyms API Error: {e}")
            return []
    
    @staticmethod
    def get_word_antonyms(word: str) -> List[str]:
        """Get antonyms using Datamuse API"""
        try:
            response = requests.get(f"https://api.datamuse.com/words?rel_ant={word}")
            if response.status_code == 200:
                data = response.json()
                return [item['word'] for item in data[:10]]  # Top 10 antonyms
            return []
        except Exception as e:
            print(f"Antonyms API Error: {e}")
            return []

class MainApplication(ctk.CTkFrame):
    """Enhanced main application with sidebar and professional UI"""
    
    def __init__(self, parent, username):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.current_theme = THEME_MODE
        self.db = DatabaseManager()
        
        # Create main layout
        self.create_layout()
        
        # Load initial page
        self.show_dashboard()
    
    def create_layout(self):
        """Create the main application layout with sidebar"""
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Sidebar
        self.create_sidebar()
        
        # Content area
        self.content_frame = ctk.CTkFrame(
            self.main_container, 
            fg_color=COLORS[self.current_theme]["secondary_bg"],
            corner_radius=15
        )
        self.content_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    def create_sidebar(self):
        """Create the professional sidebar"""
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=250,
            fg_color=COLORS[self.current_theme]["bg"],
            corner_radius=15
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        self.sidebar.pack_propagate(False)
        
        # Header with user info
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # User avatar placeholder
        avatar_label = ctk.CTkLabel(
            header_frame,
            text="👤",
            font=("Arial", 40),
            text_color=COLORS[self.current_theme]["accent"]
        )
        avatar_label.pack(pady=(0, 10))
        
        # Username
        username_label = ctk.CTkLabel(
            header_frame,
            text=self.username,
            font=("Helvetica", 18, "bold"),
            text_color=COLORS[self.current_theme]["text"]
        )
        username_label.pack()
        
        # Theme toggle button
        theme_btn = ctk.CTkButton(
            header_frame,
            text="🌙" if self.current_theme == "dark" else "☀️",
            width=40,
            height=40,
            command=self.toggle_theme,
            fg_color="transparent",
            hover_color=COLORS[self.current_theme]["accent"]
        )
        theme_btn.pack(pady=10)
        
        # Navigation menu
        self.create_navigation_menu()
        
        # Logout button at bottom
        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            width=200,
            height=40,
            fg_color="#FF5252",
            hover_color="#FF1A1A",
            command=self.logout,
            corner_radius=10
        )
        logout_btn.pack(side="bottom", pady=20, padx=20)
    
    def create_navigation_menu(self):
        """Create navigation menu items"""
        menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        menu_frame.pack(fill="x", padx=20, pady=20)
        
        # Menu items
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("👤 Profile", self.show_profile),
            ("📚 My Dictionary", self.show_dictionary),
            ("🔤 Find by Alphabet", self.show_alphabet_search),
            ("⭐ Saved Words", self.show_saved_words),
            ("🎯 Word Learning", self.show_word_learning)
        ]
        
        self.menu_buttons = []
        for text, command in menu_items:
            btn = ctk.CTkButton(
                menu_frame,
                text=text,
                width=200,
                height=40,
                command=command,
                fg_color="transparent",
                hover_color=COLORS[self.current_theme]["accent"],
                corner_radius=10,
                anchor="w"
            )
            btn.pack(pady=5, fill="x")
            self.menu_buttons.append(btn)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        ctk.set_appearance_mode(self.current_theme)
        
        # Update colors
        self.sidebar.configure(fg_color=COLORS[self.current_theme]["bg"])
        self.content_frame.configure(fg_color=COLORS[self.current_theme]["secondary_bg"])
        
        # Refresh current page
        if hasattr(self, 'current_page'):
            self.current_page.destroy()
        self.show_dashboard()
    
    def clear_content(self):
        """Clear the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Show dashboard page"""
        self.clear_content()
        self.current_page = DashboardPage(self.content_frame, self.username, self.db)

    def show_profile(self):
        """Show profile page"""
        self.clear_content()
        self.current_page = ProfilePage(self.content_frame, self.username, self.db)
    
    def show_dictionary(self):
        """Show dictionary page"""
        self.clear_content()
        self.current_page = DictionaryPage(self.content_frame, self.username, self.db)
    
    def show_alphabet_search(self):
        """Show alphabet search page"""
        self.clear_content()
        self.current_page = AlphabetSearchPage(self.content_frame, self.username, self.db)
    
    def show_saved_words(self):
        """Show saved words page"""
        self.clear_content()
        self.current_page = SavedWordsPage(self.content_frame, self.username, self.db)
    
    def show_word_learning(self):
        """Show word learning page"""
        self.clear_content()
        self.current_page = WordLearningPage(self.content_frame, self.username, self.db)

    def logout(self):
        """Logout user"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Delete remember me token
            try:
                if os.path.exists('remember.token'):
                    with open('remember.token', 'r') as f:
                        token = f.read().strip()
                    self.db.delete_remember_token(token)
                    os.remove('remember.token')
            except Exception as e:
                print(f"Error removing token: {e}")
            
            # Destroy the current page
            self.destroy()
            
            # Show login page
            LoginPage(self.master, lambda: None)

class WelcomePage(ctk.CTkFrame):
    """Legacy welcome page - redirects to new main app"""
    def __init__(self, parent, username):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        
        # Redirect to new main application
        self.destroy()
        MainApplication(self.master, username)

class DashboardPage(ctk.CTkFrame):
    """Enhanced dashboard page with animations"""
    
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Create dashboard content
        self.create_dashboard()
    
    def create_dashboard(self):
        """Create the dashboard content"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=30)
        
        welcome_label = ctk.CTkLabel(
            header_frame,
            text=f"Welcome back, {self.username}! 👋",
            font=("Helvetica", 32, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        welcome_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Ready to expand your vocabulary?",
            font=("Helvetica", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Stats cards
        self.create_stats_cards()
        
        # Quick actions
        self.create_quick_actions()
    
    def create_stats_cards(self):
        """Create statistics cards"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)
        
        # Get user stats
        try:
            conn = sqlite3.connect(self.db.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM word_history WHERE username = ?', (self.username,))
            word_count = cursor.fetchone()[0]
            conn.close()
        except:
            word_count = 0
        
        # Stats cards
        cards_data = [
            ("📚", "Total Words", str(word_count), "#4CAF50"),
            ("⭐", "Saved Words", "0", "#FF9800"),
            ("🎯", "Learning Streak", "0", "#2196F3"),
            ("📈", "Progress", "0%", "#9C27B0")
        ]
        
        for i, (icon, title, value, color) in enumerate(cards_data):
            card = ctk.CTkFrame(
                stats_frame,
                fg_color=COLORS[THEME_MODE]["bg"],
                corner_radius=15,
                border_width=1,
                border_color=color
            )
            card.pack(side="left", fill="both", expand=True, padx=5)
            
            # Card content
            icon_label = ctk.CTkLabel(card, text=icon, font=("Arial", 24))
            icon_label.pack(pady=(15, 5))
            
            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=("Helvetica", 24, "bold"),
                text_color=color
            )
            value_label.pack()
            
            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=("Helvetica", 12),
                text_color=COLORS[THEME_MODE]["text_secondary"]
            )
            title_label.pack(pady=(0, 15))
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(
            actions_frame,
            text="Quick Actions",
            font=("Helvetica", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        ).pack(anchor="w", pady=(0, 15))
        
        # Action buttons
        actions = [
            ("🔍 Search Word", "#2196F3"),
            ("📚 Browse Dictionary", "#4CAF50"),
            ("🎯 Start Learning", "#FF9800"),
            ("⭐ View Saved", "#9C27B0")
        ]
        
        for i, (text, color) in enumerate(actions):
            btn = ctk.CTkButton(
                actions_frame,
                text=text,
                width=200,
                height=50,
                fg_color=color,
                hover_color=self.darken_color(color),
                corner_radius=10,
                font=("Helvetica", 14, "bold")
            )
            btn.pack(side="left", padx=10)
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#2196F3": "#1976D2",
            "#4CAF50": "#388E3C",
            "#FF9800": "#F57C00",
            "#9C27B0": "#7B1FA2"
        }
        return color_map.get(color, color)

class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        self.notification_thread = None
        self.notification_active = False

        self.create_profile_page()
    
    def create_profile_page(self):
        """Create enhanced profile page"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=30)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👤 Profile Settings",
            font=("Helvetica", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w")
        
        # Profile info card
        profile_card = ctk.CTkFrame(
            self,
            fg_color=COLORS[THEME_MODE]["bg"],
            corner_radius=15,
            border_width=2,
            border_color=COLORS[THEME_MODE]["accent"]
        )
        profile_card.pack(fill="x", padx=30, pady=20)
        
        # Profile content
        profile_content = ctk.CTkFrame(profile_card, fg_color="transparent")
        profile_content.pack(fill="x", padx=20, pady=20)
        
        # User info
        user_info_frame = ctk.CTkFrame(profile_content, fg_color="transparent")
        user_info_frame.pack(fill="x", pady=(0, 20))
        
        # Avatar and basic info
        avatar_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        avatar_frame.pack(side="left")
        
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="👤",
            font=("Arial", 60),
            text_color=COLORS[THEME_MODE]["accent"]
        )
        avatar_label.pack()
        
        # User details
        details_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
        details_frame.pack(side="left", padx=20, fill="both", expand=True)
        
        username_label = ctk.CTkLabel(
            details_frame,
            text=f"Username: {self.username}",
            font=("Helvetica", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        username_label.pack(anchor="w", pady=(0, 5))
        
        profession = self.db.get_profession(self.username)
        profession_label = ctk.CTkLabel(
            details_frame,
            text=f"Profession: {profession}",
            font=("Helvetica", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        profession_label.pack(anchor="w")
        
        # Main container for settings
        main_frame = ctk.CTkFrame(self, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Profile header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(40, 20))
        
        profile_title = ctk.CTkLabel(
            header_frame,
            text="Profile Settings",
            font=("Helvetica", 36, "bold")
        )
        profile_title.pack()
        
        # Content area
        content_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Notification settings
        notification_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        notification_frame.pack(pady=20, padx=20, fill="x")
        
        ctk.CTkLabel(
            notification_frame,
            text="Desktop Notifications",
            font=("Helvetica", 18, "bold")
        ).pack(anchor="w", pady=(0, 10))
        
        # Notification interval
        interval_frame = ctk.CTkFrame(notification_frame, fg_color="transparent")
        interval_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            interval_frame,
            text="Notification Interval (minutes):"
        ).pack(side="left", padx=(0, 10))
        
        self.interval_var = tk.StringVar(value="30")
        self.interval_entry = ctk.CTkEntry(
            interval_frame,
            width=100,
            textvariable=self.interval_var
        )
        self.interval_entry.pack(side="left")
        
        # Notification message
        message_frame = ctk.CTkFrame(notification_frame, fg_color="transparent")
        message_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            message_frame,
            text="Notification Message:"
        ).pack(anchor="w", pady=(0, 5))
        
        self.message_var = tk.StringVar(value="Time for a break!")
        self.message_entry = ctk.CTkEntry(
            message_frame,
            width=300,
            textvariable=self.message_var
        )
        self.message_entry.pack(anchor="w")
        
        # Toggle button
        self.toggle_btn = ctk.CTkButton(
            notification_frame,
            text="Start Notifications",
            width=200,
            command=self.toggle_notifications
        )
        self.toggle_btn.pack(pady=20)
        
        # Back button
        back_btn = ctk.CTkButton(
            content_frame,
            text="Back to Dashboard",
            width=200,
            command=self.back_to_dashboard
        )
        back_btn.pack(pady=20)
        
        # --- Profile Card (top-right) ---
        db = DatabaseManager()
        profession = db.get_profession(self.username)
        profile_card = ctk.CTkFrame(main_frame, fg_color="#444", corner_radius=12, border_width=2, border_color="#fff")
        profile_card.place(relx=0.98, rely=0.25, anchor="ne")
        ctk.CTkLabel(profile_card, text=f"User: {self.username}", font=("Helvetica", 14, "bold")).pack(padx=16, pady=(10, 2))
        ctk.CTkLabel(profile_card, text=f"Profession: {profession}", font=("Helvetica", 12)).pack(padx=16, pady=(0, 10))
    
    def toggle_notifications(self):
        if not self.notification_active:
            try:
                interval = float(self.interval_var.get())
                if interval <= 0:
                    raise ValueError
                
                self.notification_active = True
                self.toggle_btn.configure(
                    text="Stop Notifications",
                    fg_color="#FF5252",
                    hover_color="#FF1A1A"
                )
                
                # Create scheduled task
                self.create_scheduled_task(interval)
                
                # Start notification thread
                self.notification_thread = threading.Thread(
                    target=self.send_notifications,
                    daemon=True
                )
                self.notification_thread.start()
                
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Please enter a valid positive number for the interval!"
                )
        else:
            self.notification_active = False
            self.toggle_btn.configure(
                text="Start Notifications",
                fg_color=["#3B8ED0", "#1F6AA5"],
                hover_color=["#36719F", "#144870"]
            )
            # Remove scheduled task
            self.remove_scheduled_task()
    
    def create_scheduled_task(self, interval):
        """Create scheduled task (Windows only)"""
        if sys.platform != "win32":
            print("Scheduled tasks are only supported on Windows")
            return
            
        try:
            import subprocess
            
            # Get the path to the Python interpreter and current script
            python_path = sys.executable
            script_path = os.path.abspath(__file__)
            
            # Create task command
            task_cmd = (
                f'schtasks /create /tn "VocabularyBooster_{self.username}" /tr "'
                f'"{python_path}" "{script_path}" --notify "{self.username}"" '
                f'/sc minute /mo {int(interval)} /f'
            )
            
            subprocess.run(task_cmd, shell=True, check=True)
            
        except Exception as e:
            print(f"Error creating scheduled task: {e}")
    
    def remove_scheduled_task(self):
        """Remove scheduled task (Windows only)"""
        if sys.platform != "win32":
            return
            
        try:
            import subprocess
            task_cmd = f'schtasks /delete /tn "VocabularyBooster_{self.username}" /f'
            subprocess.run(task_cmd, shell=True, check=True)
        except Exception as e:
            print(f"Error removing scheduled task: {e}")
    
    def send_notifications(self):
        while self.notification_active:
            try:
                # Show custom notification
                CustomNotification(self.username, self.message_var.get(), self)
                
                # Sleep for the interval
                interval_minutes = float(self.interval_var.get())
                time.sleep(interval_minutes * 60)
                
            except Exception as e:
                messagebox.showerror("Notification Error", 
                    f"Failed to send notification: {str(e)}")
                self.notification_active = False
                self.toggle_btn.configure(
                    text="Start Notifications",
                    fg_color=["#3B8ED0", "#1F6AA5"],
                    hover_color=["#36719F", "#144870"]
                )
                break
    
    def back_to_dashboard(self):
        self.notification_active = False  # Stop notifications
        self.destroy()
        WelcomePage(self.master, self.username)
    
    def show_word_learning(self):
        self.notification_active = False  # Stop notifications
        self.destroy()
        db = DatabaseManager()
        profession = db.get_profession(self.username)
        WordLearningPage(self.master, self.username, profession)
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Stop notifications
            self.notification_active = False
            if self.notification_thread:
                self.notification_thread.join(timeout=1)
            
            # Destroy the current page
            self.destroy()
            
            # Show login page
            LoginPage(self.master, lambda: None)

class WordLearningPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Get profession from database
        if hasattr(db, 'get_profession'):
            self.profession = db.get_profession(username) or "Student"
        else:
            # If db is not a DatabaseManager instance, create one
            db_manager = DatabaseManager()
            self.profession = db_manager.get_profession(username) or "Student"
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(40, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Word of the Moment",
            font=("Helvetica", 36, "bold")
        )
        title.pack()
        
        # Content area
        content_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Word display
        self.word_label = ctk.CTkLabel(
            content_frame,
            text="Generating word...",  # Changed initial text
            font=("Helvetica", 24)
        )
        self.word_label.pack(pady=30)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Generate button
        self.generate_btn = ctk.CTkButton(  # Made instance variable
            button_frame,
            text="Generate New Word",
            width=200,
            command=self.generate_word
        )
        self.generate_btn.pack(pady=10)
        
        # Search button
        self.search_btn = ctk.CTkButton(
            button_frame,
            text="Search Meaning",
            width=200,
            command=self.search_current_word,
            state="disabled"
        )
        self.search_btn.pack(pady=10)

        # Antonyms button
        self.antonyms_btn = ctk.CTkButton(
            button_frame,
            text="Antonyms",
            width=200,
            command=self.search_antonyms,
            state="disabled"
        )
        self.antonyms_btn.pack(pady=10)

        # Synonyms button
        self.synonyms_btn = ctk.CTkButton(
            button_frame,
            text="Synonyms",
            width=200,
            command=self.search_synonyms,
            state="disabled"
        )
        self.synonyms_btn.pack(pady=10)
        
        # Back button
        back_btn = ctk.CTkButton(
            button_frame,
            text="Back to Profile",
            width=200,
            command=self.back_to_profile
        )
        back_btn.pack(pady=20)
        
        self.current_word = None
        
        # Automatically generate word when page opens
        self.master.after(100, self.generate_word)  # Short delay to ensure UI is ready
    
    def generate_word(self):
        try:
            topic = profession_to_topic.get(self.profession, "general")
            response = requests.get(
                f"https://api.datamuse.com/words?topics={topic}&max=100"
            )
            if response.status_code == 200:
                data = response.json()
                print(f"API returned {len(data)} words for topic: {topic}")  # Debug line
                words = [item['word'] for item in data if len(item['word']) > 2]
                if words:
                    self.current_word = random.choice(words)
                    self.word_label.configure(
                        text=f"Word: {self.current_word} (for {self.profession})"
                    )
                    self.search_btn.configure(state="normal")
                    self.antonyms_btn.configure(state="normal")
                    self.synonyms_btn.configure(state="normal")
                else: 
                    print("No words found, trying fallback...")
                    fallback_response = requests.get(f"https://api.datamuse.com/words?ml={topic}&max=100")
                    if fallback_response.status_code == 200:
                        fallback_data = fallback_response.json()
                        fallback_words = [item['word'] for item in fallback_data if len(item['word']) > 2]
                        if fallback_words:
                            self.current_word = random.choice(fallback_words)
                            self.word_label.configure( text=f"Word: {self.current_word} " )
                            self.search_btn.configure(state="normal")
                            self.antonyms_btn.configure(state="normal")
                            self.synonyms_btn.configure(state="normal")
                        else:
                            self.word_label.configure(text="No fallback words found.")
                    else:
                         self.word_label.configure(text="Failed to fetch fallback words.")
            else:
                self.word_label.configure(text="Failed to fetch words from API.")
        except Exception as e:
            self.word_label.configure(text=f"Error: {str(e)}")
    
    def search_current_word(self):
        if self.current_word:
            # Save word to history before opening Google search
            if hasattr(self.db, 'word_history'):
            self.db.word_history(
                username=self.username,
                word=self.current_word,
                meaning=""  # Initially empty meaning, can be updated later
            )
            else:
                # If db is not a DatabaseManager instance, create one
                db_manager = DatabaseManager()
                db_manager.word_history(
                    username=self.username,
                    word=self.current_word,
                    meaning=""
                )
            
            # Open Google search for the word meaning without showing popup
            search_url = f"https://www.google.com/search?q={self.current_word}+meaning"
            webbrowser.open(search_url)
    
    def search_word(self, word):
        """Search for a specific word"""
        if word:
            search_url = f"https://www.google.com/search?q={word}+meaning"
            webbrowser.open(search_url)
    
    def search_antonyms(self):
        if self.current_word:
            search_url = f"https://www.google.com/search?q={self.current_word}+antonyms"
            webbrowser.open(search_url)

    def search_synonyms(self):
        if self.current_word:
            search_url = f"https://www.google.com/search?q={self.current_word}+synonyms"
            webbrowser.open(search_url)
    
    def back_to_profile(self):
        self.destroy()
        ProfilePage(self.master, self.username)
    
    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Destroy the current page
            self.destroy()
            
            # Show login page
            LoginPage(self.master, lambda: None)

class CustomNotification(tk.Toplevel):
    def __init__(self, username, message, parent=None):
        super().__init__()
        
        # Window settings
        self.overrideredirect(True)  # Remove window decorations
        self.attributes('-topmost', True)  # Keep window on top
        
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Window size
        width = 300
        height = 100
        
        # Position in bottom-right corner
        x = screen_width - width - 20
        y = screen_height - height - 60
        
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.configure(bg='#2b2b2b')
        
        # Add border
        border = tk.Frame(self, bg='#1f538d', width=width, height=height)
        border.place(x=0, y=0)
        
        # Content frame
        content = tk.Frame(border, bg='#2b2b2b')
        content.place(x=2, y=2, width=width-4, height=height-4)
        
        # Title
        title = tk.Label(
            content,
            text=f"Reminder for {username}",
            fg='white',
            bg='#2b2b2b',
            font=('Helvetica', 10, 'bold')
        )
        title.pack(pady=(10, 5))
        
        # Message
        msg = tk.Label(
            content,
            text=message,
            fg='white',
            bg='#2b2b2b',
            font=('Helvetica', 9)
        )
        msg.pack()
        
        # Store parent reference
        self.parent = parent
        
        # Bind click event
        self.bind('<Button-1>', self.on_click)
        title.bind('<Button-1>', self.on_click)
        msg.bind('<Button-1>', self.on_click)
        content.bind('<Button-1>', self.on_click)
        
        # Auto-close timer
        self.after(10000, self.destroy)  # Close after 10 seconds
    
    def on_click(self, event=None):
        if self.parent and hasattr(self.parent, 'show_word_learning'):
            self.parent.show_word_learning()
        self.destroy()

class AlphabetSearchPage(ctk.CTkFrame):
    """Alphabet-based word search page"""
    
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        self.create_alphabet_search()
    
    def create_alphabet_search(self):
        """Create alphabet search interface"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=30)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔤 Find Words by Alphabet",
            font=("Helvetica", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w")
        
        # Alphabet buttons
        alphabet_frame = ctk.CTkFrame(self, fg_color="transparent")
        alphabet_frame.pack(fill="x", padx=30, pady=20)
        
        ctk.CTkLabel(
            alphabet_frame,
            text="Select a letter to browse words:",
            font=("Helvetica", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        ).pack(anchor="w", pady=(0, 15))
        
        # Create alphabet buttons
        alphabet_buttons_frame = ctk.CTkFrame(alphabet_frame, fg_color="transparent")
        alphabet_buttons_frame.pack(fill="x")
        
        for i, letter in enumerate(string.ascii_uppercase):
            btn = ctk.CTkButton(
                alphabet_buttons_frame,
                text=letter,
                width=40,
                height=40,
                command=lambda l=letter: self.search_by_alphabet(l),
                fg_color=COLORS[THEME_MODE]["accent"],
                hover_color=self.darken_color(COLORS[THEME_MODE]["accent"]),
                corner_radius=8
            )
            btn.grid(row=i//6, column=i%6, padx=5, pady=5)
        
        # Results area
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS[THEME_MODE]["bg"],
            corner_radius=15
        )
        self.results_frame.pack(fill="both", expand=True, padx=30, pady=20)
    
    def search_by_alphabet(self, letter):
        """Search for words starting with the selected letter"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading_label = ctk.CTkLabel(
            self.results_frame,
            text=f"Loading words starting with '{letter}'...",
            font=("Helvetica", 16)
        )
        loading_label.pack(pady=20)
        
        # Fetch words from API
        try:
            response = requests.get(f"https://api.datamuse.com/words?sp={letter}*&max=50")
            if response.status_code == 200:
                data = response.json()
                words = [item['word'] for item in data if len(item['word']) > 2]
                
                # Clear loading
                loading_label.destroy()
                
                if words:
                    # Display words
                    ctk.CTkLabel(
                        self.results_frame,
                        text=f"Words starting with '{letter}' ({len(words)} found):",
                        font=("Helvetica", 18, "bold"),
                        text_color=COLORS[THEME_MODE]["text"]
                    ).pack(anchor="w", pady=(0, 15))
                    
                    # Create word grid
                    for i, word in enumerate(words[:30]):  # Show first 30 words
                        word_btn = ctk.CTkButton(
                            self.results_frame,
                            text=word,
                            width=120,
                            height=35,
                            command=lambda w=word: self.show_word_details(w),
                            fg_color="transparent",
                            hover_color=COLORS[THEME_MODE]["accent"],
                            corner_radius=8
                        )
                        word_btn.pack(side="left", padx=5, pady=5)
                        
                        # New line every 5 words
                        if (i + 1) % 5 == 0:
                            word_btn.pack_configure(pady=(5, 15))
                else:
                    ctk.CTkLabel(
                        self.results_frame,
                        text=f"No words found starting with '{letter}'",
                        font=("Helvetica", 16),
                        text_color=COLORS[THEME_MODE]["text_secondary"]
                    ).pack(pady=20)
            else:
                loading_label.configure(text="Error fetching words. Please try again.")
        except Exception as e:
            loading_label.configure(text=f"Error: {str(e)}")
    
    def show_word_details(self, word):
        """Show detailed information for a word"""
        # Create popup window
        popup = ctk.CTkToplevel()
        popup.title(f"Word Details: {word}")
        popup.geometry("500x400")
        popup.resizable(False, False)
        
        # Get word definition
        definition = DictionaryAPI.get_word_definition(word)
        
        if definition:
            # Word header
            word_label = ctk.CTkLabel(
                popup,
                text=word.upper(),
                font=("Helvetica", 24, "bold"),
                text_color=COLORS[THEME_MODE]["accent"]
            )
            word_label.pack(pady=20)
            
            # Phonetic
            if 'phonetic' in definition:
                phonetic_label = ctk.CTkLabel(
                    popup,
                    text=f"Pronunciation: {definition['phonetic']}",
                    font=("Helvetica", 14),
                    text_color=COLORS[THEME_MODE]["text_secondary"]
                )
                phonetic_label.pack(pady=5)
            
            # Meanings
            if 'meanings' in definition:
                meanings_frame = ctk.CTkScrollableFrame(popup, fg_color="transparent")
                meanings_frame.pack(fill="both", expand=True, padx=20, pady=10)
                
                for meaning in definition['meanings'][:3]:  # Show first 3 meanings
                    if 'partOfSpeech' in meaning:
                        pos_label = ctk.CTkLabel(
                            meanings_frame,
                            text=f"{meaning['partOfSpeech'].title()}:",
                            font=("Helvetica", 16, "bold"),
                            text_color=COLORS[THEME_MODE]["text"]
                        )
                        pos_label.pack(anchor="w", pady=(10, 5))
                    
                    if 'definitions' in meaning:
                        for i, def_item in enumerate(meaning['definitions'][:2]):  # Show first 2 definitions
                            if 'definition' in def_item:
                                def_label = ctk.CTkLabel(
                                    meanings_frame,
                                    text=f"{i+1}. {def_item['definition']}",
                                    font=("Helvetica", 12),
                                    text_color=COLORS[THEME_MODE]["text_secondary"],
                                    wraplength=400,
                                    justify="left"
                                )
                                def_label.pack(anchor="w", pady=2)
        else:
            ctk.CTkLabel(
                popup,
                text=f"No definition found for '{word}'",
                font=("Helvetica", 16),
                text_color=COLORS[THEME_MODE]["text_secondary"]
            ).pack(pady=50)
        
        # Save word button
        save_btn = ctk.CTkButton(
            popup,
            text="💾 Save Word",
            width=150,
            height=40,
            command=lambda: self.save_word(word),
            fg_color="#4CAF50",
            hover_color="#388E3C"
        )
        save_btn.pack(pady=20)
    
    def save_word(self, word):
        """Save word to user's dictionary"""
        try:
            self.db.word_history(self.username, word, "")
            messagebox.showinfo("Success", f"'{word}' has been saved to your dictionary!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save word: {str(e)}")
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#1f538d": "#1a4a7a",
            "#0078d4": "#005a9e"
        }
        return color_map.get(color, color)

class SavedWordsPage(ctk.CTkFrame):
    """Page to display and manage saved words"""
    
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        self.create_saved_words_page()
    
    def create_saved_words_page(self):
        """Create saved words interface"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=30)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="⭐ Your Saved Words",
            font=("Helvetica", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w")
        
        # Search and filter
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search your saved words...",
            width=300,
            height=35
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_words)
        
        refresh_btn = ctk.CTkButton(
            search_frame,
            text="🔄 Refresh",
            width=100,
            height=35,
            command=self.load_saved_words
        )
        refresh_btn.pack(side="left")
        
        # Words display
        self.words_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS[THEME_MODE]["bg"],
            corner_radius=15
        )
        self.words_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Load saved words
        self.load_saved_words()
    
    def load_saved_words(self):
        """Load and display saved words"""
        # Clear existing widgets
        for widget in self.words_frame.winfo_children():
            widget.destroy()
        
        try:
            conn = sqlite3.connect(self.db.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT word, meaning, searched_at 
                FROM word_history 
                WHERE username = ? 
                ORDER BY searched_at DESC
            ''', (self.username,))
            words = cursor.fetchall()
            conn.close()
            
            if not words:
                no_words_label = ctk.CTkLabel(
                    self.words_frame,
                    text="No saved words yet. Start exploring to save some words!",
                    font=("Helvetica", 16),
                    text_color=COLORS[THEME_MODE]["text_secondary"]
                )
                no_words_label.pack(pady=50)
            else:
                # Display words
                for word, meaning, searched_at in words:
                    word_card = ctk.CTkFrame(
                        self.words_frame,
                        fg_color=COLORS[THEME_MODE]["secondary_bg"],
                        corner_radius=10
                    )
                    word_card.pack(fill="x", pady=5, padx=10)
                    
                    # Word content
                    content_frame = ctk.CTkFrame(word_card, fg_color="transparent")
                    content_frame.pack(fill="x", padx=15, pady=10)
                    
                    # Word and date
                    word_info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    word_info_frame.pack(fill="x")
                    
                    word_label = ctk.CTkLabel(
                        word_info_frame,
                        text=word.upper(),
                        font=("Helvetica", 18, "bold"),
                        text_color=COLORS[THEME_MODE]["accent"]
                    )
                    word_label.pack(side="left")
                    
                    # Date
                    search_time = datetime.fromisoformat(searched_at)
                    date_str = search_time.strftime("%Y-%m-%d")
                    date_label = ctk.CTkLabel(
                        word_info_frame,
                        text=date_str,
                        font=("Helvetica", 12),
                        text_color=COLORS[THEME_MODE]["text_secondary"]
                    )
                    date_label.pack(side="right")
                    
                    # Action buttons
                    actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    actions_frame.pack(fill="x", pady=(10, 0))
                    
                    # Definition button
                    def_btn = ctk.CTkButton(
                        actions_frame,
                        text="📖 Definition",
                        width=120,
                        height=30,
                        command=lambda w=word: self.show_definition(w),
                        fg_color="#2196F3",
                        hover_color="#1976D2"
                    )
                    def_btn.pack(side="left", padx=(0, 5))
                    
                    # Synonyms button
                    syn_btn = ctk.CTkButton(
                        actions_frame,
                        text="🔄 Synonyms",
                        width=120,
                        height=30,
                        command=lambda w=word: self.show_synonyms(w),
                        fg_color="#4CAF50",
                        hover_color="#388E3C"
                    )
                    syn_btn.pack(side="left", padx=5)
                    
                    # Antonyms button
                    ant_btn = ctk.CTkButton(
                        actions_frame,
                        text="⚡ Antonyms",
                        width=120,
                        height=30,
                        command=lambda w=word: self.show_antonyms(w),
                        fg_color="#FF9800",
                        hover_color="#F57C00"
                    )
                    ant_btn.pack(side="left", padx=5)
                    
                    # Remove button
                    remove_btn = ctk.CTkButton(
                        actions_frame,
                        text="🗑️ Remove",
                        width=100,
                        height=30,
                        command=lambda w=word: self.remove_word(w),
                        fg_color="#F44336",
                        hover_color="#D32F2F"
                    )
                    remove_btn.pack(side="right")
        
        except Exception as e:
            error_label = ctk.CTkLabel(
                self.words_frame,
                text=f"Error loading words: {str(e)}",
                font=("Helvetica", 14),
                text_color="#F44336"
            )
            error_label.pack(pady=20)
    
    def filter_words(self, event):
        """Filter words based on search input"""
        search_term = self.search_entry.get().lower()
        # This is a simple implementation - you could enhance it with real-time filtering
        pass
    
    def show_definition(self, word):
        """Show word definition in a popup"""
        definition = DictionaryAPI.get_word_definition(word)
        
        popup = ctk.CTkToplevel()
        popup.title(f"Definition: {word}")
        popup.geometry("500x400")
        
        if definition and 'meanings' in definition:
            ctk.CTkLabel(
                popup,
                text=word.upper(),
                font=("Helvetica", 24, "bold")
            ).pack(pady=20)
            
            meanings_frame = ctk.CTkScrollableFrame(popup)
            meanings_frame.pack(fill="both", expand=True, padx=20)
            
            for meaning in definition['meanings'][:2]:
                if 'definitions' in meaning:
                    for def_item in meaning['definitions'][:1]:
                        ctk.CTkLabel(
                            meanings_frame,
                            text=def_item.get('definition', 'No definition available'),
                            font=("Helvetica", 12),
                            wraplength=400,
                            justify="left"
                        ).pack(anchor="w", pady=5)
        else:
            ctk.CTkLabel(
                popup,
                text="No definition found",
                font=("Helvetica", 16)
            ).pack(pady=50)
    
    def show_synonyms(self, word):
        """Show word synonyms"""
        synonyms = DictionaryAPI.get_word_synonyms(word)
        
        popup = ctk.CTkToplevel()
        popup.title(f"Synonyms: {word}")
        popup.geometry("400x300")
        
        ctk.CTkLabel(
            popup,
            text=f"Synonyms for '{word}':",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)
        
        if synonyms:
            synonyms_text = ", ".join(synonyms[:10])
            ctk.CTkLabel(
                popup,
                text=synonyms_text,
                font=("Helvetica", 12),
                wraplength=350,
                justify="left"
            ).pack(pady=10, padx=20)
        else:
            ctk.CTkLabel(
                popup,
                text="No synonyms found",
                font=("Helvetica", 14)
            ).pack(pady=50)
    
    def show_antonyms(self, word):
        """Show word antonyms"""
        antonyms = DictionaryAPI.get_word_antonyms(word)
        
        popup = ctk.CTkToplevel()
        popup.title(f"Antonyms: {word}")
        popup.geometry("400x300")
        
        ctk.CTkLabel(
            popup,
            text=f"Antonyms for '{word}':",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)
        
        if antonyms:
            antonyms_text = ", ".join(antonyms[:10])
            ctk.CTkLabel(
                popup,
                text=antonyms_text,
                font=("Helvetica", 12),
                wraplength=350,
                justify="left"
            ).pack(pady=10, padx=20)
        else:
            ctk.CTkLabel(
                popup,
                text="No antonyms found",
                font=("Helvetica", 14)
            ).pack(pady=50)
    
    def remove_word(self, word):
        """Remove word from saved words"""
        if messagebox.askyesno("Confirm", f"Remove '{word}' from your saved words?"):
            try:
                conn = sqlite3.connect(self.db.db_file)
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM word_history 
                    WHERE username = ? AND word = ?
                ''', (self.username, word))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"'{word}' has been removed from your saved words.")
                self.load_saved_words()  # Refresh the list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove word: {str(e)}")

class DictionaryPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        self.create_dictionary_page()
    
    def create_dictionary_page(self):
        """Create enhanced dictionary page with search functionality"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=30)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="📚 Dictionary Search",
            font=("Helvetica", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w")
        
        # Search section
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=20)
        
        # Search input
        search_input_frame = ctk.CTkFrame(search_frame, fg_color="transparent")
        search_input_frame.pack(fill="x", pady=(0, 15))
        
        self.search_entry = ctk.CTkEntry(
            search_input_frame,
            placeholder_text="Enter a word to search...",
            width=400,
            height=45,
            font=("Helvetica", 16)
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_word())
        
        search_btn = ctk.CTkButton(
            search_input_frame,
            text="🔍 Search",
            width=120,
            height=45,
            command=self.search_word,
            fg_color=COLORS[THEME_MODE]["accent"],
            hover_color=self.darken_color(COLORS[THEME_MODE]["accent"]),
            font=("Helvetica", 14, "bold")
        )
        search_btn.pack(side="left")
        
        # Results area
        self.results_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=COLORS[THEME_MODE]["bg"],
            corner_radius=15
        )
        self.results_frame.pack(fill="both", expand=True, padx=30, pady=20)
    
    def search_word(self):
        """Search for word definition"""
        word = self.search_entry.get().strip()
        if not word:
            messagebox.showwarning("Warning", "Please enter a word to search.")
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading_label = ctk.CTkLabel(
            self.results_frame,
            text=f"Searching for '{word}'...",
            font=("Helvetica", 16)
        )
        loading_label.pack(pady=20)
        
        # Get definition from API
        definition = DictionaryAPI.get_word_definition(word)
        
        # Clear loading
        loading_label.destroy()
        
        if definition:
            self.display_word_definition(word, definition)
        else:
            ctk.CTkLabel(
                self.results_frame,
                text=f"No definition found for '{word}'",
                font=("Helvetica", 16),
                text_color=COLORS[THEME_MODE]["text_secondary"]
            ).pack(pady=20)
    
    def display_word_definition(self, word, definition):
        """Display word definition with enhanced UI"""
        # Word header
        word_header_frame = ctk.CTkFrame(
            self.results_frame,
            fg_color=COLORS[THEME_MODE]["accent"],
            corner_radius=10
        )
        word_header_frame.pack(fill="x", pady=(0, 15))
        
        word_label = ctk.CTkLabel(
            word_header_frame,
            text=word.upper(),
            font=("Helvetica", 32, "bold"),
            text_color="white"
        )
        word_label.pack(pady=15)
        
        # Phonetic
        if 'phonetic' in definition:
            phonetic_label = ctk.CTkLabel(
                word_header_frame,
                text=f"Pronunciation: {definition['phonetic']}",
                font=("Helvetica", 14),
                text_color="white"
            )
            phonetic_label.pack(pady=(0, 15))
        
        # Meanings
        if 'meanings' in definition:
            for i, meaning in enumerate(definition['meanings'][:3]):  # Show first 3 meanings
                meaning_frame = ctk.CTkFrame(
                    self.results_frame,
                    fg_color=COLORS[THEME_MODE]["secondary_bg"],
                    corner_radius=10
                )
                meaning_frame.pack(fill="x", pady=5)
                
                # Part of speech
                if 'partOfSpeech' in meaning:
                    pos_label = ctk.CTkLabel(
                        meaning_frame,
                        text=f"{meaning['partOfSpeech'].title()}",
                        font=("Helvetica", 18, "bold"),
                        text_color=COLORS[THEME_MODE]["accent"]
                    )
                    pos_label.pack(anchor="w", padx=20, pady=(15, 5))
                
                # Definitions
                if 'definitions' in meaning:
                    for j, def_item in enumerate(meaning['definitions'][:2]):  # Show first 2 definitions
                        if 'definition' in def_item:
                            def_label = ctk.CTkLabel(
                                meaning_frame,
                                text=f"{j+1}. {def_item['definition']}",
                                font=("Helvetica", 14),
                                text_color=COLORS[THEME_MODE]["text"],
                                wraplength=600,
                                justify="left"
                            )
                            def_label.pack(anchor="w", padx=20, pady=2)
                
                # Action buttons for this meaning
                actions_frame = ctk.CTkFrame(meaning_frame, fg_color="transparent")
                actions_frame.pack(fill="x", padx=20, pady=(10, 15))
                
                # Save word button
                save_btn = ctk.CTkButton(
                    actions_frame,
                    text="💾 Save Word",
                    width=120,
                    height=35,
                    command=lambda w=word: self.save_word(w),
                    fg_color="#4CAF50",
                    hover_color="#388E3C"
                )
                save_btn.pack(side="left", padx=(0, 10))
                
                # Synonyms button
                syn_btn = ctk.CTkButton(
                    actions_frame,
                    text="🔄 Synonyms",
                    width=120,
                    height=35,
                    command=lambda w=word: self.show_synonyms(w),
                    fg_color="#2196F3",
                    hover_color="#1976D2"
                )
                syn_btn.pack(side="left", padx=10)
                
                # Antonyms button
                ant_btn = ctk.CTkButton(
                    actions_frame,
                    text="⚡ Antonyms",
                    width=120,
                    height=35,
                    command=lambda w=word: self.show_antonyms(w),
                    fg_color="#FF9800",
                    hover_color="#F57C00"
                )
                ant_btn.pack(side="left", padx=10)
    
    def save_word(self, word):
        """Save word to user's dictionary"""
        try:
            self.db.word_history(self.username, word, "")
            messagebox.showinfo("Success", f"'{word}' has been saved to your dictionary!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save word: {str(e)}")
    
    def show_synonyms(self, word):
        """Show word synonyms in popup"""
        synonyms = DictionaryAPI.get_word_synonyms(word)
        
        popup = ctk.CTkToplevel()
        popup.title(f"Synonyms: {word}")
        popup.geometry("400x300")
        
        ctk.CTkLabel(
            popup,
            text=f"Synonyms for '{word}':",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)
        
        if synonyms:
            synonyms_text = ", ".join(synonyms[:10])
            ctk.CTkLabel(
                popup,
                text=synonyms_text,
                font=("Helvetica", 12),
                wraplength=350,
                justify="left"
            ).pack(pady=10, padx=20)
        else:
            ctk.CTkLabel(
                popup,
                text="No synonyms found",
                font=("Helvetica", 14)
            ).pack(pady=50)
    
    def show_antonyms(self, word):
        """Show word antonyms in popup"""
        antonyms = DictionaryAPI.get_word_antonyms(word)
        
        popup = ctk.CTkToplevel()
        popup.title(f"Antonyms: {word}")
        popup.geometry("400x300")
        
        ctk.CTkLabel(
            popup,
            text=f"Antonyms for '{word}':",
            font=("Helvetica", 18, "bold")
        ).pack(pady=20)
        
        if antonyms:
            antonyms_text = ", ".join(antonyms[:10])
            ctk.CTkLabel(
                popup,
                text=antonyms_text,
                font=("Helvetica", 12),
                wraplength=350,
                justify="left"
            ).pack(pady=10, padx=20)
        else:
            ctk.CTkLabel(
                popup,
                text="No antonyms found",
                font=("Helvetica", 14)
            ).pack(pady=50)
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#1f538d": "#1a4a7a",
            "#0078d4": "#005a9e"
        }
        return color_map.get(color, color)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(40, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="My Dictionary",
            font=("Helvetica", 36, "bold")
        )
        title.pack()
        
        # Content area
        content_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Add word entry
        word_entry_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        word_entry_frame.pack(fill="x", padx=10, pady=10)
        
        self.word_entry = ctk.CTkEntry(
            word_entry_frame,
            placeholder_text="Enter a word",
            width=200
        )
        self.word_entry.pack(side="left", padx=5)

        add_btn = ctk.CTkButton(
            word_entry_frame,
            text="Add Word",
            width=100,
            command=self.add_word
        )
        add_btn.pack(side="left", padx=5)

        # Create scrollable frame for word history
        self.scroll_frame = ctk.CTkScrollableFrame(content_frame, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))

        # Load and display words
        self.load_words()
        
        # Back button
        back_btn = ctk.CTkButton(
            content_frame,
            text="Back to Dashboard",
            width=200,
            command=self.back_to_dashboard
        )
        back_btn.pack(pady=20)

    def load_words(self):
        # Clear existing widgets in scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            # Get word history from database
            db = DatabaseManager()
            conn = sqlite3.connect(db.db_file)
            cursor = conn.cursor()

            # Get words for this user, ordered by most recent first
            cursor.execute('''
                SELECT word, meaning, searched_at  
                FROM word_history 
                WHERE username = ? 
                ORDER BY searched_at DESC
            ''', (self.username,))
            words = cursor.fetchall()
            
            if not words:
                no_words_label = ctk.CTkLabel(
                    self.scroll_frame,
                    text="No words added yet",
                    font=("Helvetica", 14)
                )
                no_words_label.pack(pady=20)
            else:
                # Display each word with meaning and timestamp
                for word, meaning, searched_at in words:
                    word_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#1a1a1a")
                    word_frame.pack(fill="x", pady=5)

                    # Word label
                    word_label = ctk.CTkLabel(
                        word_frame,
                        text=word,
                        font=("Helvetica", 14, "bold")
                    )
                    word_label.pack(side="left", padx=(10, 5), pady=5)

                    # Buttons frame
                    buttons_frame = ctk.CTkFrame(word_frame, fg_color="transparent")
                    buttons_frame.pack(side="left", padx=5, pady=5)

                    # Meaning button
                    meaning_btn = ctk.CTkButton(
                        buttons_frame,
                        text="Meaning",
                        width=120,
                        command=lambda w=word: self.search_word(w)
                    )
                    meaning_btn.pack(side="left", padx=5)

                    # Antonyms button
                    antonyms_btn = ctk.CTkButton(
                        buttons_frame,
                        text="Antonyms",
                        width=120,
                        command=lambda w=word: self.search_antonyms(w)
                    )
                    antonyms_btn.pack(side="left", padx=5)

                    # Synonyms button
                    synonyms_btn = ctk.CTkButton(
                        buttons_frame,
                        text="Synonyms",
                        width=120,
                        command=lambda w=word: self.search_synonyms(w)
                    )
                    synonyms_btn.pack(side="left", padx=5)

                    # Timestamp (optional, right side)
                    search_time = datetime.fromisoformat(searched_at)
                    time_str = search_time.strftime("%Y-%m-%d %H:%M")
                    time_label = ctk.CTkLabel(
                        word_frame,
                        text=time_str,
                        font=("Helvetica", 12)
                    )
                    time_label.pack(side="right", padx=10, pady=5)

        except sqlite3.Error as e:
            error_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"Database error: {e}",
                font=("Helvetica", 14)
            )
            error_label.pack(pady=20)
        finally:
            if 'conn' in locals():
                conn.close()

    def add_word(self):
        word = self.word_entry.get().strip()
        if word:
            try:
                db = DatabaseManager()
                db.word_history(self.username, word, "")
                # Clear entry
                self.word_entry.delete(0, 'end')
                # Reload words display
                self.load_words()
            except Exception as e:
                print(f"Error adding word: {e}")
    
    def back_to_dashboard(self):
        self.destroy()
        WelcomePage(self.master, self.username)

    def search_word(self, word):
        """Open Google search for a word's meaning"""
        search_url = f"https://www.google.com/search?q={word}+meaning"
        webbrowser.open(search_url)

    def search_antonyms(self, word):
        search_url = f"https://www.google.com/search?q={word}+antonyms"
        webbrowser.open(search_url)

    def search_synonyms(self, word):
        search_url = f"https://www.google.com/search?q={word}+synonyms"
        webbrowser.open(search_url)

def handle_command_line():
    """Handle command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--notify", help="Username to show notification")
    args = parser.parse_args()
    
    if args.notify:
        # Show notification
        notification = CustomNotification(args.notify, "Time to learn a new word!")
        notification.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        handle_command_line()
    else:
        app = AuthenticationApp()
        app.run()
