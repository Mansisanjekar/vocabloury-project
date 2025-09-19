"""
Authentication controller for VocabLoury application
"""

import customtkinter as ctk
from views.auth_views import LoginPage, SignupPage
from views.main_views import MainApplication
from config.settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, THEME_MODE


class AuthenticationApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title(WINDOW_TITLE)
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
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
        self.window.title("Login - VocabLoury")
        
    def show_signup_page(self):
        if self.current_page:
            self.current_page.destroy()
        self.current_page = SignupPage(self.container, self.show_login_page)
        
    def run(self):
        self.window.mainloop()
