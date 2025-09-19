"""
Main application views for VocabLoury application
"""

import customtkinter as ctk
from tkinter import messagebox
import os

from models.database import DatabaseManager
from utils.icons import Icons
from config.settings import COLORS, THEME_MODE
from PIL import Image, ImageTk


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
            width=280,
            fg_color=COLORS[self.current_theme]["bg"],
            corner_radius=20
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 15))
        self.sidebar.pack_propagate(False)
        
        # Header with user info
        header_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=25)
        
        # User avatar with logo
        try:
            # Try to load the logo image
            logo_image = Image.open("static/images/logo.png")
            logo_image = logo_image.resize((80, 80), Image.Resampling.LANCZOS)
            logo_photo = ctk.CTkImage(logo_image, size=(80, 80))
            
            avatar_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
            avatar_label.image = logo_photo  # Keep a reference
            avatar_label.pack(pady=(0, 15))
        except:
            # Fallback to text avatar
            avatar_frame = ctk.CTkFrame(
                header_frame,
                width=80,
                height=80,
                fg_color=COLORS[self.current_theme]["accent"],
                corner_radius=40
            )
            avatar_frame.pack(pady=(0, 15))
            avatar_frame.pack_propagate(False)
            
            avatar_label = ctk.CTkLabel(
                avatar_frame,
                text="U",
                font=("Inter", 24, "bold"),
                text_color="white"
            )
            avatar_label.pack(expand=True)
        
        # Username
        username_label = ctk.CTkLabel(
            header_frame,
            text=self.username,
            font=("Inter", 20, "bold"),
            text_color=COLORS[self.current_theme]["text"]
        )
        username_label.pack(pady=(0, 5))
        
        # User profession
        profession_label = ctk.CTkLabel(
            header_frame,
            text="Student",  # This should be dynamic
            font=("Inter", 14),
            text_color=COLORS[self.current_theme]["text_secondary"]
        )
        profession_label.pack(pady=(0, 20))
        
        # Theme toggle button
        theme_btn = ctk.CTkButton(
            header_frame,
            text="●" if self.current_theme == "dark" else "○",
            width=45,
            height=45,
            command=self.toggle_theme,
            fg_color=COLORS[self.current_theme]["secondary_bg"],
            hover_color=COLORS[self.current_theme]["accent"],
            corner_radius=22,
            font=("Inter", 16, "bold")
        )
        theme_btn.pack(pady=(0, 20))
        
        # Navigation menu
        self.create_navigation_menu()
        
        # Logout button at bottom
        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="Logout",
            width=200,
            height=40,
            fg_color="#FF5252",
            hover_color="#FF1A1A",
            command=self.logout,
            corner_radius=10,
            font=("Inter", 12, "bold")
        )
        logout_btn.pack(side="bottom", pady=20, padx=20)
    
    def create_navigation_menu(self):
        """Create navigation menu items"""
        menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        menu_frame.pack(fill="x", padx=25, pady=20)
        
        # Menu items
        menu_items = [
            ("⌂", "Dashboard", self.show_dashboard),
            ("●", "Profile", self.show_profile),
            ("📖", "Dictionary", self.show_dictionary),
            ("A", "Alphabet Search", self.show_alphabet_search),
            ("★", "Saved Words", self.show_saved_words),
            ("●", "Word Learning", self.show_word_learning)
        ]
        
        self.menu_buttons = []
        for icon, text, command in menu_items:
            btn_frame = ctk.CTkFrame(menu_frame, fg_color="transparent")
            btn_frame.pack(fill="x", pady=3)
            
            btn = ctk.CTkButton(
                btn_frame,
                text=f"{icon}  {text}",
                height=50,
                command=command,
                fg_color="transparent",
                hover_color=COLORS[self.current_theme]["accent"],
                corner_radius=12,
                anchor="w",
                font=("Inter", 14),
                text_color=COLORS[self.current_theme]["text_secondary"]
            )
            btn.pack(fill="x")
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
            from views.auth_views import LoginPage
            LoginPage(self.master, lambda: None)


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
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Welcome section with gradient text effect
        welcome_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        welcome_container.pack(fill="x", pady=(0, 20))
        
        welcome_label = ctk.CTkLabel(
            welcome_container,
            text=f"Welcome back, {self.username}!",
            font=("Inter", 32, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        welcome_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            welcome_container,
            text="Ready to expand your vocabulary?",
            font=("Inter", 18),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        subtitle_label.pack(anchor="w", pady=(10, 0))
        
        # Stats cards
        self.create_stats_cards()
        
        # Quick actions
        self.create_quick_actions()
    
    def create_stats_cards(self):
        """Create statistics cards"""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=40, pady=30)
        
        # Get user stats
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM word_history WHERE username = ?', (self.username,))
            word_count = cursor.fetchone()[0]
            conn.close()
        except:
            word_count = 0
        
        # Stats cards
        cards_data = [
            ("📖", "Total Words", str(word_count), "#4CAF50"),
            ("★", "Saved Words", "0", "#FF9800"),
            ("●", "Learning Streak", "0", "#2196F3"),
            ("▲", "Progress", "0%", "#9C27B0")
        ]
        
        for i, (icon, title, value, color) in enumerate(cards_data):
            card = ctk.CTkFrame(
                stats_frame,
                fg_color=COLORS[THEME_MODE]["secondary_bg"],
                corner_radius=20,
                border_width=2,
                border_color=color
            )
            card.pack(side="left", fill="both", expand=True, padx=8)
            
            # Card header with accent line
            header_frame = ctk.CTkFrame(card, fg_color="transparent")
            header_frame.pack(fill="x", padx=20, pady=(20, 10))
            
            # Accent line
            accent_line = ctk.CTkFrame(header_frame, fg_color=color, height=4, corner_radius=2)
            accent_line.pack(fill="x", pady=(0, 15))
            
            # Card content
            icon_label = ctk.CTkLabel(card, text=icon, font=("Arial", 32))
            icon_label.pack(pady=(0, 10))
            
            value_label = ctk.CTkLabel(
                card,
                text=value,
                font=("Inter", 28, "bold"),
                text_color=color
            )
            value_label.pack(pady=(0, 5))
            
            title_label = ctk.CTkLabel(
                card,
                text=title,
                font=("Inter", 14),
                text_color=COLORS[THEME_MODE]["text_secondary"]
            )
            title_label.pack(pady=(0, 20))
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=40, pady=30)
        
        # Section title
        title_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="Quick Actions",
            font=("Inter", 24, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Jump into your learning journey",
            font=("Inter", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))
        
        # Action buttons container
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # Action buttons
        actions = [
            ("🔍", "Search Word", "#2196F3"),
            ("📖", "Browse Dictionary", "#4CAF50"),
            ("●", "Start Learning", "#FF9800"),
            ("★", "View Saved", "#9C27B0")
        ]
        
        for i, (icon, text, color) in enumerate(actions):
            btn_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
            btn_frame.pack(side="left", fill="both", expand=True, padx=8)
            
            btn = ctk.CTkButton(
                btn_frame,
                text=f"{icon}\n{text}",
                height=80,
                fg_color=COLORS[THEME_MODE]["secondary_bg"],
                hover_color=color,
                corner_radius=15,
                font=("Inter", 14, "bold"),
                text_color=COLORS[THEME_MODE]["text"],
                border_width=2,
                border_color=color
            )
            btn.pack(fill="both", expand=True)
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#2196F3": "#1976D2",
            "#4CAF50": "#388E3C",
            "#FF9800": "#F57C00",
            "#9C27B0": "#7B1FA2"
        }
        return color_map.get(color, color)


# Placeholder classes for other pages
class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text="Profile Page", font=("Helvetica", 24)).pack(expand=True)

class DictionaryPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text="Dictionary Page", font=("Helvetica", 24)).pack(expand=True)

class AlphabetSearchPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text="Alphabet Search Page", font=("Helvetica", 24)).pack(expand=True)

class SavedWordsPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text="Saved Words Page", font=("Helvetica", 24)).pack(expand=True)

class WordLearningPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text="Word Learning Page", font=("Helvetica", 24)).pack(expand=True)
