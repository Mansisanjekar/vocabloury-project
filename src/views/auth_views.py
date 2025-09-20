"""
Authentication views for VocabLoury application
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

from src.models.database import DatabaseManager
from src.utils.validation import FormValidator
from src.utils.animations import AnimatedBackground, AnimatedButton, darken_color
from src.utils.icons import Icons
from config.settings import COLORS, THEME_MODE


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, show_signup_callback):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.show_signup_callback = show_signup_callback
        self.validator = FormValidator()
        
        # Check for remember me token
        token = self.load_remember_token()
        if token:
            db = DatabaseManager()
            success, username = db.verify_remember_token(token)
            if success:
                self.destroy()
                from views.main_views import MainApplication
                MainApplication(self.master, username)
                return
            else:
                self.delete_remember_token()
        
        self.create_login_ui()
    
    def create_login_ui(self):
        """Create the login UI"""
        # Create animated background
        self.animated_bg = AnimatedBackground(self, fg_color="transparent")
        self.animated_bg.pack(fill="both", expand=True)
        
        # Create main container with gradient background
        main_container = ctk.CTkFrame(self.animated_bg, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create split layout with scrolling
        left_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=20)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Add scrollable frame to left side
        left_scroll = ctk.CTkScrollableFrame(left_frame, fg_color="transparent")
        left_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Add scrollable frame to right side
        right_scroll = ctk.CTkScrollableFrame(right_frame, fg_color="transparent")
        right_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left side - Login Form
        form_frame = ctk.CTkFrame(left_scroll, fg_color="transparent")
        form_frame.pack(pady=20, padx=40, expand=True)
        
        # Header with logo
        header_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        header_frame.pack(pady=(20, 40))
        
        # Logo/Icon
        try:
            # Try to load the logo image
            logo_image = Image.open("static/images/logo.png")
            logo_image = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
            logo_photo = ctk.CTkImage(logo_image, size=(60, 60))
            
            logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
            logo_label.pack(pady=(0, 20))
        except:
            # Fallback to text logo
            logo_frame = ctk.CTkFrame(header_frame, fg_color=COLORS[THEME_MODE]["accent"], 
                                    width=60, height=60, corner_radius=30)
            logo_frame.pack(pady=(0, 20))
            logo_frame.pack_propagate(False)
            
            logo_label = ctk.CTkLabel(logo_frame, text="V", font=("Inter", 24, "bold"), text_color="white")
            logo_label.pack(expand=True)
        
        # Title
        title = ctk.CTkLabel(header_frame, text="Welcome Back!", 
                           font=("Inter", 32, "bold"),
                           text_color=COLORS[THEME_MODE]["text"])
        title.pack(pady=(0, 10))
        
        subtitle = ctk.CTkLabel(header_frame, text="Login to your account", 
                             font=("Inter", 16),
                             text_color=COLORS[THEME_MODE]["text_secondary"])
        subtitle.pack()
        
        # Form fields container
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(pady=20, fill="x")
        
        # Username field
        username_container = ctk.CTkFrame(fields_frame, fg_color="transparent")
        username_container.pack(fill="x", pady=(0, 12))
        
        username_label = ctk.CTkLabel(username_container, text="Username", 
                                    font=("Inter", 12, "bold"),
                                    text_color=COLORS[THEME_MODE]["text"])
        username_label.pack(anchor="w", pady=(0, 4))
        
        self.username = ctk.CTkEntry(username_container, placeholder_text="Enter your username",
                                   height=40, corner_radius=8, 
                                   font=("Inter", 13),
                                   border_width=1,
                                   border_color=COLORS[THEME_MODE]["border"])
        self.username.pack(fill="x")
        self.username.bind("<FocusOut>", self.validate_username_field)
        
        # Username error label
        self.username_error = ctk.CTkLabel(username_container, text="", 
                                         text_color="#FF5252", font=("Inter", 10))
        self.username_error.pack(anchor="w", pady=(2, 0))
        
        # Password field
        password_container = ctk.CTkFrame(fields_frame, fg_color="transparent")
        password_container.pack(fill="x", pady=(0, 12))
        
        password_label = ctk.CTkLabel(password_container, text="Password", 
                                    font=("Inter", 12, "bold"),
                                    text_color=COLORS[THEME_MODE]["text"])
        password_label.pack(anchor="w", pady=(0, 4))
        
        self.password = ctk.CTkEntry(password_container, placeholder_text="Enter your password",
                                   height=40, corner_radius=8, show="•",
                                   font=("Inter", 13),
                                   border_width=1,
                                   border_color=COLORS[THEME_MODE]["border"])
        self.password.pack(fill="x")
        self.password.bind("<FocusOut>", self.validate_password_field)
        
        # Password error label
        self.password_error = ctk.CTkLabel(password_container, text="", 
                                         text_color="#FF5252", font=("Inter", 10))
        self.password_error.pack(anchor="w", pady=(2, 0))
        
        # Remember me checkbox
        remember_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        remember_frame.pack(fill="x", pady=(8, 16))
        
        self.remember = ctk.CTkCheckBox(remember_frame, text="Remember me",
                                      font=("Inter", 12),
                                      text_color=COLORS[THEME_MODE]["text_secondary"])
        self.remember.pack(anchor="w")
        
        # Login button with animation
        login_button = AnimatedButton(fields_frame, text="Login", height=42,
                                    corner_radius=8, 
                                    command=self.login,
                                    font=("Inter", 14, "bold"),
                                    fg_color=COLORS[THEME_MODE]["accent"],
                                    hover_color=darken_color(COLORS[THEME_MODE]["accent"]))
        login_button.pack(fill="x", pady=(16, 20))
        
        # Signup link
        signup_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        signup_frame.pack(pady=(0, 16))
        
        signup_label = ctk.CTkLabel(signup_frame, text="Don't have an account?",
                                  font=("Inter", 12),
                                  text_color=COLORS[THEME_MODE]["text_secondary"])
        signup_label.pack(side="left", padx=(0, 8))
        
        signup_button = AnimatedButton(signup_frame, text="Sign Up",
                                     command=self.show_signup_callback,
                                     fg_color="transparent", 
                                     hover_color=COLORS[THEME_MODE]["accent"],
                                     text_color=COLORS[THEME_MODE]["accent"],
                                     font=("Inter", 12, "bold"))
        signup_button.pack(side="left")
        
        # Forgot password link
        forgot_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        forgot_frame.pack(pady=10)
        
        forgot_button = AnimatedButton(forgot_frame, text="Forgot Password?",
                                     command=self.show_forgot_password,
                                     fg_color="transparent", 
                                     hover_color=COLORS[THEME_MODE]["accent"],
                                     text_color=COLORS[THEME_MODE]["text_secondary"],
                                     font=("Inter", 12))
        forgot_button.pack()
        
        # Right side - Project Information
        self.create_project_info(right_scroll)
    
    def create_project_info(self, parent):
        """Create project information with typing animation"""
        from src.utils.animations import TypingAnimation
        
        # Header
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # App icon
        try:
            logo_image = Image.open("app_icon_64.png")
            logo_photo = ctk.CTkImage(logo_image, size=(80, 80))
            logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
            logo_label.pack(pady=(0, 20))
        except:
            # Fallback icon
            icon_frame = ctk.CTkFrame(header_frame, fg_color=COLORS[THEME_MODE]["accent"], 
                                    width=80, height=80, corner_radius=40)
            icon_frame.pack(pady=(0, 20))
            icon_frame.pack_propagate(False)
            
            icon_label = ctk.CTkLabel(icon_frame, text="V", font=("Inter", 32, "bold"), text_color="white")
            icon_label.pack(expand=True)
        
        # App title
        title_label = ctk.CTkLabel(header_frame, text="VocabLoury", 
                                 font=("Inter", 28, "bold"),
                                 text_color=COLORS[THEME_MODE]["text"])
        title_label.pack(pady=(0, 10))
        
        # Typing animation for subtitle
        subtitle_label = ctk.CTkLabel(header_frame, text="", 
                                    font=("Inter", 16),
                                    text_color=COLORS[THEME_MODE]["text_secondary"])
        subtitle_label.pack(pady=(0, 30))
        
        # Start typing animation
        typing_animation = TypingAnimation(subtitle_label, "Professional Dictionary & Learning App", 80)
        typing_animation.start()
        
        # Features section
        features_frame = ctk.CTkFrame(parent, fg_color="transparent")
        features_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        features_title = ctk.CTkLabel(features_frame, text="Features", 
                                    font=("Inter", 20, "bold"),
                                    text_color=COLORS[THEME_MODE]["text"])
        features_title.pack(anchor="w", pady=(0, 20))
        
        # Features list
        features = [
            "-> Comprehensive Dictionary",
            "-> Alphabet Search",
            "-> Save Favorite Words",
            "-> Personalized Learning",
            "-> Progress Tracking",
            "-> Dark Theme"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(features_frame, text=feature,
                                       font=("Inter", 14),
                                       text_color=COLORS[THEME_MODE]["text_secondary"],
                                       anchor="w")
            feature_label.pack(fill="x", pady=5)
    
    def show_forgot_password(self):
        """Show forgot password dialog"""
        from tkinter import messagebox, simpledialog
        
        email = simpledialog.askstring("Forgot Password", 
                                     "Enter your email address to reset password:")
        if email:
            # Here you would implement actual password reset logic
            messagebox.showinfo("Password Reset", 
                              f"Password reset instructions sent to {email}")
    
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
    
    def login(self):
        username = self.username.get().strip()
        password = self.password.get()
        
        # Quick validation
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        # Show loading state
        self.show_loading_state()
        
        try:
            # Use existing db instance or create one
            if not hasattr(self, 'db'):
                self.db = DatabaseManager()
            
            success, user_id = self.db.verify_user(username, password)
            
            if success:
                # Handle remember me
                if self.remember.get():
                    token = self.db.create_remember_token(user_id)
                    if token:
                        self.save_remember_token(token)
                
                # Quick transition to main app
                self.destroy()
                from views.main_views import MainApplication
                MainApplication(self.master, username)
            else:
                self.hide_loading_state()
                messagebox.showerror("Error", "Invalid username or password!")
                
        except Exception as e:
            self.hide_loading_state()
            messagebox.showerror("Error", f"Login failed: {str(e)}")
    
    def show_loading_state(self):
        """Show loading state during login"""
        # Disable login button and show loading
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton) and "Login" in widget.cget("text"):
                widget.configure(text="Logging in...", state="disabled")
                break
    
    def hide_loading_state(self):
        """Hide loading state"""
        # Re-enable login button
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton) and "Logging in" in widget.cget("text"):
                widget.configure(text="Login", state="normal")
                break
    
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


class SignupPage(ctk.CTkFrame):
    def __init__(self, parent, show_login_callback):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.show_login_callback = show_login_callback
        self.validator = FormValidator()
        
        self.create_signup_ui()
    
    def create_signup_ui(self):
        """Create the signup UI"""
        # Create animated background
        self.animated_bg = AnimatedBackground(self, fg_color="transparent")
        self.animated_bg.pack(fill="both", expand=True)
        
        # Create main container with gradient background
        main_container = ctk.CTkFrame(self.animated_bg, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create split layout with scrolling
        left_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=20)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Add scrollable frame to left side
        left_scroll = ctk.CTkScrollableFrame(left_frame, fg_color="transparent")
        left_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=20)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Add scrollable frame to right side
        right_scroll = ctk.CTkScrollableFrame(right_frame, fg_color="transparent")
        right_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left side - Signup Form
        form_frame = ctk.CTkFrame(left_scroll, fg_color="transparent")
        form_frame.pack(pady=20, padx=50, expand=True)
        
        # Header with logo
        header_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        header_frame.pack(pady=(20, 30))
        
        # Logo/Icon
        try:
            # Try to load the logo image
            logo_image = Image.open("static/images/logo.png")
            logo_image = logo_image.resize((60, 60), Image.Resampling.LANCZOS)
            logo_photo = ctk.CTkImage(logo_image, size=(60, 60))
            
            logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
            logo_label.pack(pady=(0, 20))
        except:
            # Fallback to text logo
            logo_frame = ctk.CTkFrame(header_frame, fg_color=COLORS[THEME_MODE]["accent"], 
                                    width=60, height=60, corner_radius=30)
            logo_frame.pack(pady=(0, 20))
            logo_frame.pack_propagate(False)
            
            logo_label = ctk.CTkLabel(logo_frame, text="V", font=("Inter", 24, "bold"), text_color="white")
            logo_label.pack(expand=True)
        
        # Title
        title = ctk.CTkLabel(header_frame, text="Create Account", 
                           font=("Inter", 28, "bold"),
                           text_color=COLORS[THEME_MODE]["text"])
        title.pack(pady=(0, 8))
        
        subtitle = ctk.CTkLabel(header_frame, text="Sign up to get started", 
                             font=("Inter", 16),
                             text_color=COLORS[THEME_MODE]["text_secondary"])
        subtitle.pack()
        
        # Form fields container
        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(pady=20, fill="x")
        
        # Username field
        username_container = ctk.CTkFrame(fields_frame, fg_color="transparent")
        username_container.pack(fill="x", pady=(0, 10))
        
        username_label = ctk.CTkLabel(username_container, text="Username", 
                                    font=("Inter", 12, "bold"),
                                    text_color=COLORS[THEME_MODE]["text"])
        username_label.pack(anchor="w", pady=(0, 4))
        
        self.username = ctk.CTkEntry(username_container, placeholder_text="Enter your username",
                                   height=38, corner_radius=8, 
                                   font=("Inter", 13),
                                   border_width=1,
                                   border_color=COLORS[THEME_MODE]["border"])
        self.username.pack(fill="x")
        self.username.bind("<FocusOut>", self.validate_username_field)
        
        self.username_error = ctk.CTkLabel(username_container, text="", 
                                         text_color="#FF5252", font=("Inter", 10))
        self.username_error.pack(anchor="w", pady=(2, 0))
        
        # Email field
        email_container = ctk.CTkFrame(fields_frame, fg_color="transparent")
        email_container.pack(fill="x", pady=(0, 10))
        
        email_label = ctk.CTkLabel(email_container, text="Email", 
                                 font=("Inter", 12, "bold"),
                                 text_color=COLORS[THEME_MODE]["text"])
        email_label.pack(anchor="w", pady=(0, 4))
        
        self.email = ctk.CTkEntry(email_container, placeholder_text="Enter your email",
                                height=38, corner_radius=8, 
                                font=("Inter", 13),
                                border_width=1,
                                border_color=COLORS[THEME_MODE]["border"])
        self.email.pack(fill="x")
        self.email.bind("<FocusOut>", self.validate_email_field)
        
        self.email_error = ctk.CTkLabel(email_container, text="", 
                                      text_color="#FF5252", font=("Inter", 10))
        self.email_error.pack(anchor="w", pady=(2, 0))
        
        # Profession dropdown
        profession_container = ctk.CTkFrame(fields_frame, fg_color="transparent")
        profession_container.pack(fill="x", pady=(0, 10))
        
        profession_label = ctk.CTkLabel(profession_container, text="Profession", 
                                      font=("Inter", 12, "bold"),
                                      text_color=COLORS[THEME_MODE]["text"])
        profession_label.pack(anchor="w", pady=(0, 4))
        
        self.profession_var = tk.StringVar()
        self.profession_dropdown = ctk.CTkComboBox(
            profession_container,
            values=["", "Student", "Entrepreneur", "Scientist", "Musician", "Writer"],
            variable=self.profession_var,
            height=38,
            corner_radius=8,
            font=("Inter", 13),
            border_width=1,
            border_color=COLORS[THEME_MODE]["border"]
        )
        self.profession_dropdown.pack(fill="x")
        self.profession_dropdown.bind("<<ComboboxSelected>>", self.validate_profession_field)
        
        self.profession_error = ctk.CTkLabel(profession_container, text="", 
                                           text_color="#FF5252", font=("Inter", 10))
        self.profession_error.pack(anchor="w", pady=(2, 0))
        
        # Password field
        password_container = ctk.CTkFrame(fields_frame, fg_color="transparent")
        password_container.pack(fill="x", pady=(0, 10))
        
        password_label = ctk.CTkLabel(password_container, text="Password", 
                                    font=("Inter", 12, "bold"),
                                    text_color=COLORS[THEME_MODE]["text"])
        password_label.pack(anchor="w", pady=(0, 4))
        
        self.password = ctk.CTkEntry(password_container, placeholder_text="Enter your password",
                                   height=38, corner_radius=8, show="•",
                                   font=("Inter", 13),
                                   border_width=1,
                                   border_color=COLORS[THEME_MODE]["border"])
        self.password.pack(fill="x")
        self.password.bind("<FocusOut>", self.validate_password_field)
        
        self.password_error = ctk.CTkLabel(password_container, text="", 
                                         text_color="#FF5252", font=("Inter", 10))
        self.password_error.pack(anchor="w", pady=(2, 0))
        
        # Confirm Password field
        confirm_password_container = ctk.CTkFrame(fields_frame, fg_color="transparent")
        confirm_password_container.pack(fill="x", pady=(0, 10))
        
        confirm_password_label = ctk.CTkLabel(confirm_password_container, text="Confirm Password", 
                                            font=("Inter", 12, "bold"),
                                            text_color=COLORS[THEME_MODE]["text"])
        confirm_password_label.pack(anchor="w", pady=(0, 4))
        
        self.confirm_password = ctk.CTkEntry(confirm_password_container, placeholder_text="Confirm your password",
                                          height=38, corner_radius=8, show="•",
                                          font=("Inter", 13),
                                          border_width=1,
                                          border_color=COLORS[THEME_MODE]["border"])
        self.confirm_password.pack(fill="x")
        self.confirm_password.bind("<FocusOut>", self.validate_confirm_password_field)
        
        self.confirm_password_error = ctk.CTkLabel(confirm_password_container, text="", 
                                                 text_color="#FF5252", font=("Inter", 10))
        self.confirm_password_error.pack(anchor="w", pady=(2, 0))
        
        # Terms and conditions
        terms_frame = ctk.CTkFrame(fields_frame, fg_color="transparent")
        terms_frame.pack(fill="x", pady=(10, 0))
        
        self.terms_checkbox = ctk.CTkCheckBox(terms_frame, text="I agree to the Terms and Conditions",
                                            font=("Inter", 11),
                                            text_color=COLORS[THEME_MODE]["text_secondary"])
        self.terms_checkbox.pack(anchor="w")
        
        # Sign up button with animation
        signup_button = AnimatedButton(fields_frame, text="Create Account", height=45,
                                     corner_radius=10, 
                                     command=self.signup,
                                     font=("Inter", 16, "bold"),
                                     fg_color=COLORS[THEME_MODE]["accent"],
                                     hover_color=darken_color(COLORS[THEME_MODE]["accent"]))
        signup_button.pack(fill="x", pady=(20, 20))
        
        # Login link
        login_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        login_frame.pack(pady=(0, 16))
        
        login_label = ctk.CTkLabel(login_frame, text="Already have an account?",
                                 font=("Inter", 12),
                                 text_color=COLORS[THEME_MODE]["text_secondary"])
        login_label.pack(side="left", padx=(0, 8))
        
        login_button = AnimatedButton(login_frame, text="Login",
                                    command=self.show_login_callback,
                                    fg_color="transparent", 
                                    hover_color=COLORS[THEME_MODE]["accent"],
                                    text_color=COLORS[THEME_MODE]["accent"],
                                    font=("Inter", 12, "bold"))
        login_button.pack(side="left")
        
        # Right side - Project Information
        self.create_project_info(right_scroll)
    
    def create_project_info(self, parent):
        """Create project information with typing animation"""
        from src.utils.animations import TypingAnimation
        
        # Header
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # App icon
        try:
            logo_image = Image.open("app_icon_64.png")
            logo_photo = ctk.CTkImage(logo_image, size=(80, 80))
            logo_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
            logo_label.pack(pady=(0, 20))
        except:
            # Fallback icon
            icon_frame = ctk.CTkFrame(header_frame, fg_color=COLORS[THEME_MODE]["accent"], 
                                    width=80, height=80, corner_radius=40)
            icon_frame.pack(pady=(0, 20))
            icon_frame.pack_propagate(False)
            
            icon_label = ctk.CTkLabel(icon_frame, text="V", font=("Inter", 32, "bold"), text_color="white")
            icon_label.pack(expand=True)
        
        # App title
        title_label = ctk.CTkLabel(header_frame, text="VocabLoury", 
                                 font=("Inter", 28, "bold"),
                                 text_color=COLORS[THEME_MODE]["text"])
        title_label.pack(pady=(0, 10))
        
        # Typing animation for subtitle
        subtitle_label = ctk.CTkLabel(header_frame, text="", 
                                    font=("Inter", 16),
                                    text_color=COLORS[THEME_MODE]["text_secondary"])
        subtitle_label.pack(pady=(0, 30))
        
        # Start typing animation
        typing_animation = TypingAnimation(subtitle_label, "Join thousands of learners!", 80)
        typing_animation.start()
        
        # Features section
        features_frame = ctk.CTkFrame(parent, fg_color="transparent")
        features_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        features_title = ctk.CTkLabel(features_frame, text="Why Choose VocabLoury?", 
                                    font=("Inter", 20, "bold"),
                                    text_color=COLORS[THEME_MODE]["text"])
        features_title.pack(anchor="w", pady=(0, 20))
        
        # Features list
        features = [
            "✓ Comprehensive Dictionary",
            "✓ Alphabet Search",
            "✓ Save Favorite Words",
            "✓ Personalized Learning",
            "✓ Progress Tracking",
            "✓ Professional UI"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(features_frame, text=feature,
                                       font=("Inter", 14),
                                       text_color=COLORS[THEME_MODE]["text_secondary"],
                                       anchor="w")
            feature_label.pack(fill="x", pady=5)
        
        # Stats section
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", padx=40, pady=(0, 40))
        
        stats_title = ctk.CTkLabel(stats_frame, text="Join Our Community", 
                                 font=("Inter", 18, "bold"),
                                 text_color=COLORS[THEME_MODE]["text"])
        stats_title.pack(anchor="w", pady=(0, 15))
        
        # Stats
        stats = [
            ("1000+", "Active Users"),
            ("50K+", "Words Searched"),
            ("4.8★", "User Rating")
        ]
        
        for value, label in stats:
            stat_frame = ctk.CTkFrame(stats_frame, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=10)
            stat_frame.pack(fill="x", pady=5)
            
            stat_value = ctk.CTkLabel(stat_frame, text=value,
                                    font=("Inter", 16, "bold"),
                                    text_color=COLORS[THEME_MODE]["accent"])
            stat_value.pack(anchor="w", padx=15, pady=(10, 0))
            
            stat_label = ctk.CTkLabel(stat_frame, text=label,
                                    font=("Inter", 12),
                                    text_color=COLORS[THEME_MODE]["text_secondary"])
            stat_label.pack(anchor="w", padx=15, pady=(0, 10))
    
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
    
    def signup(self):
        username = self.username.get().strip()
        email = self.email.get().strip()
        password = self.password.get()
        confirm_password = self.confirm_password.get()
        profession = self.profession_var.get()
        terms_accepted = self.terms_checkbox.get()
        
        # Quick validation
        if not all([username, email, password, confirm_password, profession]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        if not terms_accepted:
            messagebox.showerror("Terms Required", "Please accept the Terms and Conditions to continue.")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        
        # Show loading state
        self.show_signup_loading_state()
        
        try:
            # Use existing db instance or create one
            if not hasattr(self, 'db'):
                self.db = DatabaseManager()
            
            success, message = self.db.create_user(username, email, password, profession)
            
            if success:
                messagebox.showinfo("Success", "Account created successfully!")
                self.show_login_callback()
            else:
                self.hide_signup_loading_state()
                messagebox.showerror("Error", message)
                
        except Exception as e:
            self.hide_signup_loading_state()
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
    
    def show_signup_loading_state(self):
        """Show loading state during signup"""
        # Disable signup button and show loading
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton) and "Create Account" in widget.cget("text"):
                widget.configure(text="Creating Account...", state="disabled")
                break
    
    def hide_signup_loading_state(self):
        """Hide loading state"""
        # Re-enable signup button
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton) and "Creating Account" in widget.cget("text"):
                widget.configure(text="Create Account", state="normal")
                break
    
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
