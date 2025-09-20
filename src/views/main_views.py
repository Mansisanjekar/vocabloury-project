"""
Main application views for VocabLoury application
"""

import customtkinter as ctk
from tkinter import messagebox
import os

from src.models.database import DatabaseManager
from src.utils.icons import Icons
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
        
        # Create scrollable frame for sidebar content
        self.sidebar_scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.sidebar_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Header with user info
        header_frame = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=25)
        
        # User avatar with logo
        try:
            # Try to load the logo image
            logo_image = Image.open("static/images/logo.png")
            logo_image = logo_image.resize((80, 80), Image.Resampling.LANCZOS)
            logo_photo = ctk.CTkImage(logo_image, size=(80, 80))
            
            avatar_label = ctk.CTkLabel(header_frame, image=logo_photo, text="")
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
        
        # Bottom buttons frame
        bottom_frame = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=25, pady=(20, 25))
        
        # Theme toggle button
        theme_btn = ctk.CTkButton(
            bottom_frame,
            text="🌙 Dark Mode" if self.current_theme == "light" else "☀️ Light Mode",
            width=200,
            height=40,
            fg_color=COLORS[self.current_theme]["accent"],
            hover_color=COLORS[self.current_theme]["accent"],
            command=self.toggle_theme,
            corner_radius=10,
            font=("Inter", 12, "bold")
        )
        theme_btn.pack(pady=(0, 10))
        
        logout_btn = ctk.CTkButton(
            bottom_frame,
            text="Logout",
            width=200,
            height=40,
            fg_color="#FF5252",
            hover_color="#FF1A1A",
            command=self.logout,
            corner_radius=10,
            font=("Inter", 12, "bold")
        )
        logout_btn.pack()
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        # Toggle theme
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        
        # Update customtkinter appearance
        ctk.set_appearance_mode(self.current_theme)
        
        # Recreate the entire layout with new theme
        self.main_container.destroy()
        self.create_layout()
        
        # Reload current page
        if hasattr(self, 'current_page_method'):
            self.current_page_method()
        else:
            self.show_dashboard()
    
    def create_navigation_menu(self):
        """Create navigation menu items"""
        menu_frame = ctk.CTkFrame(self.sidebar_scroll, fg_color="transparent")
        menu_frame.pack(fill="x", padx=25, pady=20)
        
        # Menu items
        menu_items = [
            ("⌂", "Dashboard", self.show_dashboard),
            ("👤", "Profile", self.show_profile),
            ("📖", "Dictionary", self.show_dictionary),
            ("🔤", "Alphabet Search", self.show_alphabet_search),
            ("★", "Saved Words", self.show_saved_words),
            ("🎯", "Word Learning", self.show_word_learning),
            ("📰", "Articles", self.show_articles),
            ("🔔", "Notifications", self.show_notifications),
            ("💡", "Tips", self.show_tips)
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
        self.current_page_method = self.show_dashboard
    
    def show_profile(self):
        """Show profile page"""
        self.clear_content()
        self.current_page = ProfilePage(self.content_frame, self.username, self.db)
        self.current_page_method = self.show_profile
    
    def show_dictionary(self):
        """Show dictionary page"""
        self.clear_content()
        self.current_page = DictionaryPage(self.content_frame, self.username, self.db)
        self.current_page_method = self.show_dictionary
    
    def show_alphabet_search(self):
        """Show alphabet search page"""
        self.clear_content()
        self.current_page = AlphabetSearchPage(self.content_frame, self.username, self.db)
        self.current_page_method = self.show_alphabet_search
    
    def show_saved_words(self):
        """Show saved words page"""
        self.clear_content()
        self.current_page = SavedWordsPage(self.content_frame, self.username, self.db)
        self.current_page_method = self.show_saved_words
    
    def show_word_learning(self):
        """Show word learning page"""
        self.clear_content()
        self.current_page = WordLearningPage(self.content_frame, self.username, self.db)
        self.current_page_method = self.show_word_learning
    
    def show_notifications(self):
        """Show notifications page"""
        self.clear_content()
        self.current_page = NotificationsPage(self.content_frame, self.username, self.db)
        self.current_page_method = self.show_notifications
    
    def show_tips(self):
        """Show tips page"""
        self.clear_content()
        self.current_page = TipsPage(self.content_frame, self.username, self.db)
        self.current_page_method = self.show_tips
    
    def show_articles(self):
        """Show articles page"""
        self.clear_content()
        self.current_page = ArticlesPage(self.content_frame, self.username, self.db)
        self.current_page_method = self.show_articles
    
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
        
        # Get current theme from settings
        from config.settings import THEME_MODE
        self.current_theme = THEME_MODE
        
        # Import API for floating words
        from src.api.dictionary_api import DictionaryAPI
        self.dictionary_api = DictionaryAPI()
        
        # Create dashboard content
        self.create_dashboard()
    
    def create_dashboard(self):
        """Create the dashboard content"""
        # Create scrollable frame for dashboard content
        scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
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
        
        # Floating words animation
        self.create_floating_words_section(scrollable_frame)
        
        # Stats cards
        self.create_enhanced_stats_cards(scrollable_frame)
        
        # Charts section
        self.create_charts_section()
        
        # Quick actions
        self.create_quick_actions()
    
    def create_floating_words_section(self, parent):
        """Create floating words animation section"""
        # Floating words container
        floating_frame = ctk.CTkFrame(parent, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        floating_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Section title
        title_label = ctk.CTkLabel(
            floating_frame,
            text="Word of the Moment",
            font=("Inter", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(pady=(20, 10))
        
        # Floating words canvas
        self.floating_canvas = ctk.CTkFrame(floating_frame, fg_color="transparent", height=80)
        self.floating_canvas.pack(fill="x", padx=20, pady=(0, 20))
        self.floating_canvas.pack_propagate(False)
        
        # Start floating words animation
        self.start_floating_words()
    
    def start_floating_words(self):
        """Start the floating words animation"""
        self.floating_words = []
        self.current_word_index = 0
        self.word_data = self.get_random_words()
        self.animate_floating_word()
    
    def get_random_words(self):
        """Get random words for floating animation from multiple sources"""
        words = []
        
        # Get words from multiple topics
        topics = [
            "education", "technology", "science", "art", "nature", "business", 
            "medicine", "philosophy", "literature", "psychology", "history", "mathematics"
        ]
        
        for topic in topics:
            try:
                topic_words = self.dictionary_api.get_words_by_topic(topic, 10)
                for word in topic_words[:2]:  # Take 2 from each topic
                    # Get definition for each word
                    definition = self.dictionary_api.get_word_definition(word)
                    if definition and 'meanings' in definition and definition['meanings']:
                        meaning = definition['meanings'][0]
                        if 'definitions' in meaning and meaning['definitions']:
                            def_text = meaning['definitions'][0].get('definition', 'No definition available')
                            words.append({
                                'word': word, 
                                'definition': def_text[:100] + "..." if len(def_text) > 100 else def_text
                            })
                    else:
                        # Fallback meaning
                        words.append({'word': word, 'definition': f'A word related to {topic}'})
            except Exception as e:
                print(f"Error getting words for topic {topic}: {e}")
                continue
        
        # If we don't have enough words from API, add some curated words
        if len(words) < 20:
            curated_words = [
                {'word': 'Serendipity', 'definition': 'The occurrence of happy or beneficial events by chance'},
                {'word': 'Ephemeral', 'definition': 'Lasting for a very short time'},
                {'word': 'Ubiquitous', 'definition': 'Present, appearing, or found everywhere'},
                {'word': 'Eloquent', 'definition': 'Fluent or persuasive in speaking or writing'},
                {'word': 'Resilient', 'definition': 'Able to withstand or recover quickly from difficult conditions'},
                {'word': 'Mellifluous', 'definition': 'Sweet or musical; pleasant to hear'},
                {'word': 'Petrichor', 'definition': 'The pleasant smell of earth after rain'},
                {'word': 'Wanderlust', 'definition': 'A strong desire to travel and explore the world'},
                {'word': 'Nostalgia', 'definition': 'A sentimental longing for the past'},
                {'word': 'Euphoria', 'definition': 'A feeling of intense excitement and happiness'},
                {'word': 'Zenith', 'definition': 'The highest point reached by a celestial object'},
                {'word': 'Catharsis', 'definition': 'The process of releasing strong emotions'},
                {'word': 'Panacea', 'definition': 'A solution or remedy for all problems'},
                {'word': 'Quintessential', 'definition': 'Representing the most perfect example of a quality'},
                {'word': 'Luminous', 'definition': 'Full of or shedding light; bright or shining'},
                {'word': 'Ethereal', 'definition': 'Extremely delicate and light in a way that seems too perfect for this world'},
                {'word': 'Vivacious', 'definition': 'Attractively lively and animated'},
                {'word': 'Perspicacious', 'definition': 'Having a ready insight into and understanding of things'},
                {'word': 'Sagacious', 'definition': 'Having or showing keen mental discernment and good judgment'},
                {'word': 'Magnanimous', 'definition': 'Very generous or forgiving, especially toward a rival or less powerful person'}
            ]
            words.extend(curated_words)
        
        return words[:30]  # Return up to 30 words
    
    def animate_floating_word(self):
        """Animate floating word from right to left"""
        if not self.word_data:
            return
        
        # Clear previous word
        for widget in self.floating_canvas.winfo_children():
            widget.destroy()
        
        # Get current word
        word_info = self.word_data[self.current_word_index % len(self.word_data)]
        
        # Create word display
        word_frame = ctk.CTkFrame(self.floating_canvas, fg_color="transparent")
        word_frame.pack(fill="both", expand=True)
        
        # Word
        word_label = ctk.CTkLabel(
            word_frame,
            text=word_info['word'].upper(),
            font=("Inter", 24, "bold"),
            text_color=COLORS[THEME_MODE]["accent"]
        )
        word_label.pack(pady=(10, 5))
        
        # Definition
        definition_label = ctk.CTkLabel(
            word_frame,
            text=word_info['definition'],
            font=("Inter", 12),
            text_color=COLORS[THEME_MODE]["text_secondary"],
            wraplength=800,
            justify="center"
        )
        definition_label.pack(pady=(0, 10))
        
        # Move to next word
        self.current_word_index += 1
        
        # Schedule next word (change every 4 seconds)
        self.after(4000, self.animate_floating_word)
    
    def create_enhanced_stats_cards(self, parent):
        """Create enhanced statistics cards with better data"""
        stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", padx=40, pady=30)
        
        # Get user stats
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_file)
            cursor = conn.cursor()
            
            # Total words searched
            cursor.execute('SELECT COUNT(*) FROM word_history WHERE username = ?', (self.username,))
            total_words = cursor.fetchone()[0]
            
            # Unique words
            cursor.execute('SELECT COUNT(DISTINCT word) FROM word_history WHERE username = ?', (self.username,))
            unique_words = cursor.fetchone()[0]
            
            # Learning streak (days with at least one word)
            cursor.execute('''
                SELECT COUNT(DISTINCT DATE(searched_at)) 
                FROM word_history 
                WHERE username = ? AND searched_at >= date('now', '-30 days')
            ''', (self.username,))
            learning_streak = cursor.fetchone()[0]
            
            # Progress percentage (based on unique words)
            progress = min(100, (unique_words / 100) * 100)  # Assuming 100 words = 100% progress
            
            conn.close()
        except:
            total_words = 0
            unique_words = 0
            learning_streak = 0
            progress = 0
        
        # Enhanced stats cards with professional colors
        if self.current_theme == "dark":
            cards_data = [
                ("📖", "Total Searches", str(total_words), "#4CAF50"),
                ("🔤", "Unique Words", str(unique_words), "#2196F3"),
                ("🔥", "Learning Streak", f"{learning_streak} days", "#FF9800"),
                ("📈", "Progress", f"{progress:.0f}%", "#9C27B0")
            ]
        else:
            cards_data = [
                ("📖", "Total Searches", str(total_words), "#4CAF50"),
                ("🔤", "Unique Words", str(unique_words), "#2196F3"),
                ("🔥", "Learning Streak", f"{learning_streak} days", "#FF9800"),
                ("📈", "Progress", f"{progress:.0f}%", "#9C27B0")
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
    
    def create_charts_section(self):
        """Create enhanced charts section with multiple visual data representations"""
        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.pack(fill="x", padx=40, pady=30)
        
        # Charts title
        charts_title = ctk.CTkLabel(
            charts_frame,
            text="Learning Analytics & Insights",
            font=("Inter", 24, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        charts_title.pack(anchor="w", pady=(0, 20))
        
        # Top row charts
        top_charts_container = ctk.CTkFrame(charts_frame, fg_color="transparent")
        top_charts_container.pack(fill="x", pady=(0, 15))
        
        # Chart 1 - Word Categories Distribution
        chart1 = ctk.CTkFrame(top_charts_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        chart1.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        chart1_title = ctk.CTkLabel(
            chart1,
            text="📊 Word Categories",
            font=("Inter", 16, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        chart1_title.pack(pady=(15, 10))
        
        # Enhanced bar chart with more categories
        categories = ["General", "Academic", "Technical", "Creative", "Scientific", "Business"]
        values = [30, 25, 20, 15, 7, 3]  # Mock data
        colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336", "#00BCD4"]
        
        for i, (category, value, color) in enumerate(zip(categories, values, colors)):
            bar_frame = ctk.CTkFrame(chart1, fg_color="transparent")
            bar_frame.pack(fill="x", padx=15, pady=3)
            
            # Category and value labels
            label_frame = ctk.CTkFrame(bar_frame, fg_color="transparent")
            label_frame.pack(fill="x")
            
            cat_label = ctk.CTkLabel(
                label_frame,
                text=category,
                font=("Inter", 11),
                text_color=COLORS[THEME_MODE]["text_secondary"]
            )
            cat_label.pack(side="left")
            
            val_label = ctk.CTkLabel(
                label_frame,
                text=f"{value}%",
                font=("Inter", 11, "bold"),
                text_color=color
            )
            val_label.pack(side="right")
            
            # Enhanced progress bar
            progress_frame = ctk.CTkFrame(bar_frame, fg_color=COLORS[THEME_MODE]["bg"], height=10, corner_radius=5)
            progress_frame.pack(fill="x", pady=(3, 8))
            
            progress_fill = ctk.CTkFrame(progress_frame, fg_color=color, height=10, corner_radius=5)
            progress_fill.place(relx=0, rely=0, relwidth=value/100, relheight=1)
        
        # Chart 2 - Learning Streak
        chart2 = ctk.CTkFrame(top_charts_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        chart2.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        chart2_title = ctk.CTkLabel(
            chart2,
            text="🔥 Learning Streak",
            font=("Inter", 16, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        chart2_title.pack(pady=(15, 10))
        
        # Streak visualization
        streak_frame = ctk.CTkFrame(chart2, fg_color="transparent")
        streak_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Current streak
        current_streak = ctk.CTkLabel(
            streak_frame,
            text="7",
            font=("Inter", 36, "bold"),
            text_color="#FF9800"
        )
        current_streak.pack(pady=(10, 5))
        
        streak_label = ctk.CTkLabel(
            streak_frame,
            text="Days in a row",
            font=("Inter", 12),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        streak_label.pack()
        
        # Streak calendar representation
        calendar_frame = ctk.CTkFrame(streak_frame, fg_color="transparent")
        calendar_frame.pack(fill="x", pady=(15, 10))
        
        # Create 7-day streak visualization
        for i in range(7):
            day_frame = ctk.CTkFrame(
                calendar_frame, 
                fg_color="#4CAF50" if i < 7 else COLORS[THEME_MODE]["border"],
                width=25, 
                height=25, 
                corner_radius=12
            )
            day_frame.pack(side="left", padx=2)
            day_frame.pack_propagate(False)
        
        # Bottom row charts
        bottom_charts_container = ctk.CTkFrame(charts_frame, fg_color="transparent")
        bottom_charts_container.pack(fill="x")
        
        # Chart 3 - Weekly Progress
        chart3 = ctk.CTkFrame(bottom_charts_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        chart3.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        chart3_title = ctk.CTkLabel(
            chart3,
            text="📈 Weekly Progress",
            font=("Inter", 16, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        chart3_title.pack(pady=(15, 10))
        
        # Weekly data
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        daily_words = [12, 18, 15, 22, 8, 25, 16]  # Mock data
        max_words = max(daily_words)
        
        for day, words in zip(days, daily_words):
            day_frame = ctk.CTkFrame(chart3, fg_color="transparent")
            day_frame.pack(fill="x", padx=15, pady=2)
            
            # Day label
            day_label = ctk.CTkLabel(
                day_frame,
                text=day,
                font=("Inter", 10),
                text_color=COLORS[THEME_MODE]["text_secondary"],
                width=30
            )
            day_label.pack(side="left")
            
            # Words count
            words_label = ctk.CTkLabel(
                day_frame,
                text=str(words),
                font=("Inter", 10, "bold"),
                text_color="#2196F3",
                width=30
            )
            words_label.pack(side="right")
            
            # Progress bar
            progress_frame = ctk.CTkFrame(day_frame, fg_color=COLORS[THEME_MODE]["bg"], height=6, corner_radius=3)
            progress_frame.pack(fill="x", pady=(2, 5))
            
            progress_fill = ctk.CTkFrame(progress_frame, fg_color="#2196F3", height=6, corner_radius=3)
            progress_fill.place(relx=0, rely=0, relwidth=words/max_words, relheight=1)
        
        # Chart 4 - Achievement Badges
        chart4 = ctk.CTkFrame(bottom_charts_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        chart4.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        chart4_title = ctk.CTkLabel(
            chart4,
            text="🏆 Achievements",
            font=("Inter", 16, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        chart4_title.pack(pady=(15, 10))
        
        # Achievement badges
        achievements = [
            ("🎯", "First Word", "Learned your first word"),
            ("📚", "Scholar", "Learned 50 words"),
            ("🔥", "Streak Master", "7-day learning streak"),
            ("⭐", "Vocabulary Star", "Mastered 100 words")
        ]
        
        for emoji, title, desc in achievements:
            badge_frame = ctk.CTkFrame(chart4, fg_color="transparent")
            badge_frame.pack(fill="x", padx=15, pady=5)
            
            # Badge content
            badge_content = ctk.CTkFrame(badge_frame, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=8)
            badge_content.pack(fill="x", pady=2)
            
            # Badge icon and text
            badge_text_frame = ctk.CTkFrame(badge_content, fg_color="transparent")
            badge_text_frame.pack(fill="x", padx=10, pady=8)
            
            badge_icon = ctk.CTkLabel(
                badge_text_frame,
                text=emoji,
                font=("Inter", 16)
            )
            badge_icon.pack(side="left", padx=(0, 10))
            
            badge_info = ctk.CTkFrame(badge_text_frame, fg_color="transparent")
            badge_info.pack(side="left", fill="x", expand=True)
            
            badge_title = ctk.CTkLabel(
                badge_info,
                text=title,
                font=("Inter", 12, "bold"),
                text_color=COLORS[THEME_MODE]["text"]
            )
            badge_title.pack(anchor="w")
            
            badge_desc = ctk.CTkLabel(
                badge_info,
                text=desc,
                font=("Inter", 10),
                text_color=COLORS[THEME_MODE]["text_secondary"]
            )
            badge_desc.pack(anchor="w")
    
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
        self.username = username
        self.db = db
        
        # Get current theme
        from config.settings import THEME_MODE
        self.current_theme = THEME_MODE
        
        # Create profile content
        self.create_profile()
    
    def get_user_data(self):
        """Get real user data from database"""
        try:
            import sqlite3
            conn = sqlite3.connect(self.db.db_file)
            cursor = conn.cursor()
            
            # Get user info
            cursor.execute('SELECT email, profession, created_at FROM accounts WHERE username = ?', (self.username,))
            user_data = cursor.fetchone()
            
            # Get learning stats
            cursor.execute('SELECT COUNT(*) FROM word_history WHERE username = ?', (self.username,))
            total_words = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT word) FROM word_history WHERE username = ?', (self.username,))
            unique_words = cursor.fetchone()[0]
            
            # Get last activity
            cursor.execute('SELECT MAX(timestamp) FROM word_history WHERE username = ?', (self.username,))
            last_activity = cursor.fetchone()[0]
            
            conn.close()
            
            if user_data:
                email, profession, created_at = user_data
                return {
                    'email': email,
                    'profession': profession,
                    'created_at': created_at,
                    'total_words': total_words,
                    'unique_words': unique_words,
                    'last_activity': last_activity
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None
    
    def create_profile(self):
        """Create the enhanced profile page content"""
        # Get real user data
        user_data = self.get_user_data()
        
        # Create scrollable frame for profile content
        scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Profile title
        title_label = ctk.CTkLabel(
            header_frame,
            text="👤 Profile Settings",
            font=("Inter", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Main content container
        main_container = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Left side - Personal Info
        left_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Personal info section
        personal_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        personal_frame.pack(fill="x", padx=30, pady=30)
        
        # Section title
        personal_title = ctk.CTkLabel(
            personal_frame,
            text="📋 Personal Information",
            font=("Inter", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        personal_title.pack(anchor="w", pady=(0, 20))
        
        # User avatar
        avatar_frame = ctk.CTkFrame(personal_frame, fg_color="transparent")
        avatar_frame.pack(fill="x", pady=(0, 20))
        
        # Avatar circle
        avatar_circle = ctk.CTkFrame(
            avatar_frame,
            width=80,
            height=80,
            fg_color=COLORS[THEME_MODE]["accent"],
            corner_radius=40
        )
        avatar_circle.pack(side="left")
        avatar_circle.pack_propagate(False)
        
        avatar_text = ctk.CTkLabel(
            avatar_circle,
            text=self.username[0].upper() if self.username else "U",
            font=("Inter", 24, "bold"),
            text_color="white"
        )
        avatar_text.pack(expand=True)
        
        # User details
        details_frame = ctk.CTkFrame(avatar_frame, fg_color="transparent")
        details_frame.pack(side="left", fill="x", expand=True, padx=(20, 0))
        
        # Username
        username_label = ctk.CTkLabel(
            details_frame,
            text=f"@{self.username}",
            font=("Inter", 18, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        username_label.pack(anchor="w", pady=(0, 5))
        
        # Email
        email_text = user_data['email'] if user_data else "Not available"
        email_label = ctk.CTkLabel(
            details_frame,
            text=f"📧 {email_text}",
            font=("Inter", 14),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        email_label.pack(anchor="w", pady=2)
        
        # Profession
        profession_text = user_data['profession'] if user_data else "Not specified"
        profession_label = ctk.CTkLabel(
            details_frame,
            text=f"💼 {profession_text}",
            font=("Inter", 14),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        profession_label.pack(anchor="w", pady=2)
        
        # Member since
        if user_data and user_data['created_at']:
            join_date = user_data['created_at'][:10]  # Get date part
        else:
            join_date = "2024"
        join_date_label = ctk.CTkLabel(
            details_frame,
            text=f"📅 Member since: {join_date}",
            font=("Inter", 14),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        join_date_label.pack(anchor="w", pady=2)
        
        # Right side - Learning Stats
        right_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Stats section
        stats_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=30)
        
        # Section title
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="📊 Learning Statistics",
            font=("Inter", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        stats_title.pack(anchor="w", pady=(0, 20))
        
        # Stats cards
        stats_data = [
            ("📖", "Total Words", str(user_data['total_words']) if user_data else "0", "#4CAF50"),
            ("🔤", "Unique Words", str(user_data['unique_words']) if user_data else "0", "#2196F3"),
            ("📅", "Last Activity", user_data['last_activity'][:10] if user_data and user_data['last_activity'] else "Never", "#FF9800"),
            ("⭐", "Learning Level", self.get_learning_level(user_data['total_words'] if user_data else 0), "#9C27B0")
        ]
        
        for i, (icon, title, value, color) in enumerate(stats_data):
            stat_card = ctk.CTkFrame(stats_frame, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=10)
            stat_card.pack(fill="x", pady=5)
            
            stat_content = ctk.CTkFrame(stat_card, fg_color="transparent")
            stat_content.pack(fill="x", padx=15, pady=10)
            
            # Icon and title
            icon_title_frame = ctk.CTkFrame(stat_content, fg_color="transparent")
            icon_title_frame.pack(fill="x")
            
            icon_label = ctk.CTkLabel(
                icon_title_frame,
                text=icon,
                font=("Inter", 16)
            )
            icon_label.pack(side="left")
            
            title_label = ctk.CTkLabel(
                icon_title_frame,
                text=title,
                font=("Inter", 12, "bold"),
                text_color=COLORS[THEME_MODE]["text"]
            )
            title_label.pack(side="left", padx=(10, 0))
            
            # Value
            value_label = ctk.CTkLabel(
                stat_content,
                text=value,
                font=("Inter", 16, "bold"),
                text_color=color
            )
            value_label.pack(anchor="w", pady=(5, 0))
        
        # Settings section
        settings_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        settings_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        settings_title = ctk.CTkLabel(
            settings_frame,
            text="⚙️ Account Settings",
            font=("Inter", 18, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        settings_title.pack(anchor="w", pady=(0, 15))
        
        # Settings buttons
        settings_buttons = [
            ("🔔", "Notification Settings", self.open_notification_settings),
            ("🎨", "Theme Preferences", self.open_theme_settings),
            ("🔒", "Privacy Settings", self.open_privacy_settings),
            ("📤", "Export Data", self.export_user_data)
        ]
        
        for icon, text, command in settings_buttons:
            btn = ctk.CTkButton(
                settings_frame,
                text=f"{icon} {text}",
                font=("Inter", 14),
                fg_color=COLORS[THEME_MODE]["accent"],
                hover_color=COLORS[THEME_MODE]["accent"],
                command=command,
                anchor="w"
            )
            btn.pack(fill="x", pady=3)
    
    def get_learning_level(self, total_words):
        """Get learning level based on total words"""
        if total_words >= 1000:
            return "Expert"
        elif total_words >= 500:
            return "Advanced"
        elif total_words >= 100:
            return "Intermediate"
        elif total_words >= 10:
            return "Beginner"
        else:
            return "New Learner"
    
    def open_notification_settings(self):
        """Open notification settings"""
        from tkinter import messagebox
        messagebox.showinfo("Notification Settings", "Notification settings will be available soon!")
    
    def open_theme_settings(self):
        """Open theme settings"""
        from tkinter import messagebox
        messagebox.showinfo("Theme Settings", "Theme settings will be available soon!")
    
    def open_privacy_settings(self):
        """Open privacy settings"""
        from tkinter import messagebox
        messagebox.showinfo("Privacy Settings", "Privacy settings will be available soon!")
    
    def export_user_data(self):
        """Export user data"""
        from tkinter import messagebox
        messagebox.showinfo("Export Data", "Data export feature will be available soon!")

class DictionaryPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Import API
        from api.dictionary_api import DictionaryAPI
        self.dictionary_api = DictionaryAPI()
        
        # Create dictionary content
        self.create_dictionary()
    
    def create_dictionary(self):
        """Create the dictionary page content"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Dictionary title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Dictionary",
            font=("Inter", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Search section
        search_frame = ctk.CTkFrame(self, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=15)
        search_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Search input
        self.search_input = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter a word to search...",
            height=50,
            font=("Inter", 16),
            corner_radius=10
        )
        self.search_input.pack(fill="x", padx=30, pady=30)
        self.search_input.bind("<Return>", lambda e: self.search_word())
        
        # Search button
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            height=40,
            width=120,
            font=("Inter", 14, "bold"),
            fg_color=COLORS[THEME_MODE]["accent"],
            hover_color=COLORS[THEME_MODE]["accent"],
            command=self.search_word
        )
        search_btn.pack(pady=(0, 30))
        
        # Results section
        self.results_frame = ctk.CTkFrame(self, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=15)
        self.results_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Results label
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Search results will appear here",
            font=("Inter", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        self.results_label.pack(expand=True)
    
    def search_word(self):
        """Search for a word definition"""
        word = self.search_input.get().strip()
        if not word:
            return
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading_label = ctk.CTkLabel(
            self.results_frame,
            text="Searching...",
            font=("Inter", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        loading_label.pack(expand=True)
        self.results_frame.update()
        
        # Search for word definition
        definition_data = self.dictionary_api.get_word_definition(word)
        
        if definition_data:
            # Save to word history
            self.db.word_history(self.username, word, "Searched")
            
            # Display results
            self.display_word_results(word, definition_data)
        else:
            # Show error
            error_label = ctk.CTkLabel(
                self.results_frame,
                text=f"Word '{word}' not found. Please check spelling and try again.",
                font=("Inter", 16),
                text_color="#FF5252"
            )
            error_label.pack(expand=True)
    
    def display_word_results(self, word, data):
        """Display word search results"""
        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(self.results_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Word title
        word_label = ctk.CTkLabel(
            scrollable_frame,
            text=word.upper(),
            font=("Inter", 32, "bold"),
            text_color=COLORS[THEME_MODE]["accent"]
        )
        word_label.pack(anchor="w", pady=(0, 20))
        
        # Phonetic
        if 'phonetic' in data:
            phonetic_label = ctk.CTkLabel(
                scrollable_frame,
                text=f"Pronunciation: {data['phonetic']}",
                font=("Inter", 16),
                text_color=COLORS[THEME_MODE]["text_secondary"]
            )
            phonetic_label.pack(anchor="w", pady=(0, 20))
        
        # Meanings
        if 'meanings' in data:
            for i, meaning in enumerate(data['meanings']):
                # Part of speech
                pos_label = ctk.CTkLabel(
                    scrollable_frame,
                    text=f"{i+1}. {meaning.get('partOfSpeech', 'Unknown')}",
                    font=("Inter", 20, "bold"),
                    text_color=COLORS[THEME_MODE]["text"]
                )
                pos_label.pack(anchor="w", pady=(20, 10))
                
                # Definitions
                if 'definitions' in meaning:
                    for j, definition in enumerate(meaning['definitions'][:3]):  # Show first 3 definitions
                        def_frame = ctk.CTkFrame(scrollable_frame, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=10)
                        def_frame.pack(fill="x", pady=5)
                        
                        # Definition text
                        def_text = f"• {definition.get('definition', 'No definition available')}"
                        def_label = ctk.CTkLabel(
                            def_frame,
                            text=def_text,
                            font=("Inter", 14),
                            text_color=COLORS[THEME_MODE]["text"],
                            wraplength=800,
                            justify="left"
                        )
                        def_label.pack(anchor="w", padx=15, pady=10)
                        
                        # Example
                        if 'example' in definition:
                            example_text = f"Example: {definition['example']}"
                            example_label = ctk.CTkLabel(
                                def_frame,
                                text=example_text,
                                font=("Inter", 12, "italic"),
                                text_color=COLORS[THEME_MODE]["text_secondary"],
                                wraplength=800,
                                justify="left"
                            )
                            example_label.pack(anchor="w", padx=15, pady=(0, 10))
        
        # Synonyms and Antonyms
        synonyms = self.dictionary_api.get_word_synonyms(word)
        antonyms = self.dictionary_api.get_word_antonyms(word)
        
        if synonyms or antonyms:
            # Synonyms
            if synonyms:
                syn_frame = ctk.CTkFrame(scrollable_frame, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=10)
                syn_frame.pack(fill="x", pady=10)
                
                syn_label = ctk.CTkLabel(
                    syn_frame,
                    text=f"Synonyms: {', '.join(synonyms[:5])}",
                    font=("Inter", 14),
                    text_color="#4CAF50",
                    wraplength=800,
                    justify="left"
                )
                syn_label.pack(anchor="w", padx=15, pady=10)
            
            # Antonyms
            if antonyms:
                ant_frame = ctk.CTkFrame(scrollable_frame, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=10)
                ant_frame.pack(fill="x", pady=10)
                
                ant_label = ctk.CTkLabel(
                    ant_frame,
                    text=f"Antonyms: {', '.join(antonyms[:5])}",
                    font=("Inter", 14),
                    text_color="#FF5252",
                    wraplength=800,
                    justify="left"
                )
                ant_label.pack(anchor="w", padx=15, pady=10)

class AlphabetSearchPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Import API
        from api.dictionary_api import DictionaryAPI
        self.dictionary_api = DictionaryAPI()
        
        # Create alphabet search content
        self.create_alphabet_search()
    
    def create_alphabet_search(self):
        """Create the alphabet search page content"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Alphabet Search",
            font=("Inter", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Alphabet grid
        alphabet_frame = ctk.CTkFrame(self, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=15)
        alphabet_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        # Create alphabet buttons
        alphabet_buttons_frame = ctk.CTkFrame(alphabet_frame, fg_color="transparent")
        alphabet_buttons_frame.pack(fill="x", padx=30, pady=30)
        
        # Alphabet letters
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(alphabet):
            row = i // 6
            col = i % 6
            
            btn = ctk.CTkButton(
                alphabet_buttons_frame,
                text=letter,
                width=60,
                height=60,
                font=("Inter", 20, "bold"),
                fg_color=COLORS[THEME_MODE]["accent"],
                hover_color=COLORS[THEME_MODE]["accent"],
                command=lambda l=letter: self.search_by_letter(l)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
        
        # Results section
        self.results_frame = ctk.CTkFrame(self, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=15)
        self.results_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Results label
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Click a letter to see words starting with that letter",
            font=("Inter", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        self.results_label.pack(expand=True)
    
    def search_by_letter(self, letter):
        """Search for words starting with the selected letter"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading_label = ctk.CTkLabel(
            self.results_frame,
            text=f"Loading words starting with '{letter}'...",
            font=("Inter", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        loading_label.pack(expand=True)
        self.results_frame.update()
        
        # Search for words
        words = self.dictionary_api.get_words_by_alphabet(letter.lower(), 50)
        
        if words:
            # Display results
            self.display_words_results(letter, words)
        else:
            # Show error
            error_label = ctk.CTkLabel(
                self.results_frame,
                text=f"No words found starting with '{letter}'",
                font=("Inter", 16),
                text_color="#FF5252"
            )
            error_label.pack(expand=True)
    
    def display_words_results(self, letter, words):
        """Display words starting with the selected letter"""
        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(self.results_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_label = ctk.CTkLabel(
            scrollable_frame,
            text=f"Words starting with '{letter.upper()}' ({len(words)} found)",
            font=("Inter", 24, "bold"),
            text_color=COLORS[THEME_MODE]["accent"]
        )
        header_label.pack(anchor="w", pady=(0, 20))
        
        # Words grid
        words_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        words_frame.pack(fill="x")
        
        # Display words in a grid
        for i, word in enumerate(words):
            row = i // 4
            col = i % 4
            
            word_btn = ctk.CTkButton(
                words_frame,
                text=word,
                width=120,
                height=40,
                font=("Inter", 12),
                fg_color=COLORS[THEME_MODE]["secondary_bg"],
                hover_color=COLORS[THEME_MODE]["accent"],
                command=lambda w=word: self.view_word_definition(w)
            )
            word_btn.grid(row=row, column=col, padx=5, pady=5)
    
    def view_word_definition(self, word):
        """View definition of a selected word"""
        # Save to word history
        self.db.word_history(self.username, word, "Alphabet Search")
        
        # Show word in a simple dialog
        from tkinter import messagebox
        messagebox.showinfo(f"Word: {word}", f"You selected: {word}\n\nThis would open the dictionary page to show the full definition.")

class SavedWordsPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Create saved words content
        self.create_saved_words()
    
    def create_saved_words(self):
        """Create the saved words page content"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Saved Words",
            font=("Inter", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="Refresh",
            width=100,
            height=35,
            font=("Inter", 12, "bold"),
            fg_color=COLORS[THEME_MODE]["accent"],
            hover_color=COLORS[THEME_MODE]["accent"],
            command=self.load_saved_words
        )
        refresh_btn.pack(anchor="e", pady=(0, 20))
        
        # Words list
        self.words_frame = ctk.CTkFrame(self, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=15)
        self.words_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Load saved words
        self.load_saved_words()
    
    def load_saved_words(self):
        """Load and display saved words from database"""
        # Clear previous content
        for widget in self.words_frame.winfo_children():
            widget.destroy()
        
        try:
            # Get word history from database
            import sqlite3
            import os
            
            # Get database path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_file = os.path.join(base_dir, "authentication.db")
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Get unique words searched by user
            cursor.execute('''
                SELECT DISTINCT word, COUNT(*) as search_count, MAX(searched_at) as last_searched
                FROM word_history 
                WHERE username = ? 
                GROUP BY word 
                ORDER BY last_searched DESC
            ''', (self.username,))
            
            words_data = cursor.fetchall()
            conn.close()
            
            if words_data:
                # Create scrollable frame
                scrollable_frame = ctk.CTkScrollableFrame(self.words_frame, fg_color="transparent")
                scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                # Header
                header_label = ctk.CTkLabel(
                    scrollable_frame,
                    text=f"Your Word History ({len(words_data)} words)",
                    font=("Inter", 20, "bold"),
                    text_color=COLORS[THEME_MODE]["accent"]
                )
                header_label.pack(anchor="w", pady=(0, 20))
                
                # Display words
                for word, count, last_searched in words_data:
                    word_frame = ctk.CTkFrame(scrollable_frame, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=10)
                    word_frame.pack(fill="x", pady=5)
                    
                    # Word content
                    content_frame = ctk.CTkFrame(word_frame, fg_color="transparent")
                    content_frame.pack(fill="x", padx=15, pady=10)
                    
                    # Word name
                    word_label = ctk.CTkLabel(
                        content_frame,
                        text=word.upper(),
                        font=("Inter", 18, "bold"),
                        text_color=COLORS[THEME_MODE]["text"]
                    )
                    word_label.pack(anchor="w")
                    
                    # Search info
                    info_label = ctk.CTkLabel(
                        content_frame,
                        text=f"Searched {count} time(s) • Last: {last_searched[:10]}",
                        font=("Inter", 12),
                        text_color=COLORS[THEME_MODE]["text_secondary"]
                    )
                    info_label.pack(anchor="w", pady=(5, 0))
                    
                    # Action buttons
                    button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
                    button_frame.pack(anchor="e", pady=(10, 0))
                    
                    # View definition button
                    view_btn = ctk.CTkButton(
                        button_frame,
                        text="View Definition",
                        width=120,
                        height=30,
                        font=("Inter", 11),
                        fg_color=COLORS[THEME_MODE]["accent"],
                        hover_color=COLORS[THEME_MODE]["accent"],
                        command=lambda w=word: self.view_word_definition(w)
                    )
                    view_btn.pack(side="right", padx=(5, 0))
                    
                    # Remove button
                    remove_btn = ctk.CTkButton(
                        button_frame,
                        text="Remove",
                        width=80,
                        height=30,
                        font=("Inter", 11),
                        fg_color="#FF5252",
                        hover_color="#D32F2F",
                        command=lambda w=word: self.remove_word(w)
                    )
                    remove_btn.pack(side="right")
            else:
                # No words found
                no_words_label = ctk.CTkLabel(
                    self.words_frame,
                    text="No words in your history yet.\nStart searching for words to see them here!",
                    font=("Inter", 16),
                    text_color=COLORS[THEME_MODE]["text_secondary"]
                )
                no_words_label.pack(expand=True)
                
        except Exception as e:
            # Error loading words
            error_label = ctk.CTkLabel(
                self.words_frame,
                text=f"Error loading words: {str(e)}",
                font=("Inter", 16),
                text_color="#FF5252"
            )
            error_label.pack(expand=True)
    
    def view_word_definition(self, word):
        """View definition of a selected word"""
        from tkinter import messagebox
        messagebox.showinfo(f"Word: {word}", f"You selected: {word}\n\nThis would open the dictionary page to show the full definition.")
    
    def remove_word(self, word):
        """Remove a word from history"""
        try:
            import sqlite3
            import os
            
            # Get database path
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_file = os.path.join(base_dir, "authentication.db")
            
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            
            # Remove word from history
            cursor.execute('DELETE FROM word_history WHERE username = ? AND word = ?', (self.username, word))
            conn.commit()
            conn.close()
            
            # Refresh the display
            self.load_saved_words()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to remove word: {str(e)}")

class WordLearningPage(ctk.CTkFrame):
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Import API
        from api.dictionary_api import DictionaryAPI
        self.dictionary_api = DictionaryAPI()
        
        # Get user profession
        self.profession = self.db.get_profession(username) or "Student"
        
        # Create word learning content
        self.create_word_learning()
    
    def create_word_learning(self):
        """Create the word learning page content"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Word Learning",
            font=("Inter", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w", pady=(0, 10))
        
        # Subtitle with profession
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=f"Personalized for {self.profession}s",
            font=("Inter", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        subtitle_label.pack(anchor="w", pady=(0, 20))
        
        # Control buttons
        controls_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        controls_frame.pack(fill="x", pady=(0, 20))
        
        # Generate new words button
        generate_btn = ctk.CTkButton(
            controls_frame,
            text="Generate New Words",
            width=150,
            height=35,
            font=("Inter", 12, "bold"),
            fg_color=COLORS[THEME_MODE]["accent"],
            hover_color=COLORS[THEME_MODE]["accent"],
            command=self.generate_profession_words
        )
        generate_btn.pack(side="left")
        
        # Learning content
        self.learning_frame = ctk.CTkFrame(self, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=15)
        self.learning_frame.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Initial content
        self.show_initial_content()
    
    def show_initial_content(self):
        """Show initial learning content"""
        # Clear previous content
        for widget in self.learning_frame.winfo_children():
            widget.destroy()
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            self.learning_frame,
            text=f"Welcome to Word Learning!\n\nAs a {self.profession}, you'll learn words relevant to your field.\n\nClick 'Generate New Words' to start learning!",
            font=("Inter", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"],
            justify="center"
        )
        welcome_label.pack(expand=True)
    
    def generate_profession_words(self):
        """Generate words based on user's profession"""
        # Clear previous content
        for widget in self.learning_frame.winfo_children():
            widget.destroy()
        
        # Show loading
        loading_label = ctk.CTkLabel(
            self.learning_frame,
            text=f"Generating words for {self.profession}s...",
            font=("Inter", 16),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        loading_label.pack(expand=True)
        self.learning_frame.update()
        
        # Get profession-specific topics
        topics = self.get_profession_topics()
        
        # Generate words for each topic
        all_words = []
        for topic in topics:
            words = self.dictionary_api.get_words_by_topic(topic, 10)
            all_words.extend(words[:5])  # Take first 5 words from each topic
        
        # Remove duplicates and limit to 20 words
        unique_words = list(set(all_words))[:20]
        
        if unique_words:
            self.display_learning_words(unique_words)
        else:
            self.show_error_message()
    
    def get_profession_topics(self):
        """Get topics relevant to user's profession"""
        profession_topics = {
            "Student": ["education", "study", "learning", "academic", "research"],
            "Entrepreneur": ["business", "innovation", "leadership", "strategy", "finance"],
            "Scientist": ["research", "experiment", "analysis", "discovery", "technology"],
            "Musician": ["music", "performance", "composition", "rhythm", "harmony"],
            "Writer": ["literature", "creativity", "expression", "narrative", "communication"],
            "Other": ["general", "common", "useful", "important", "interesting"]
        }
        
        return profession_topics.get(self.profession, profession_topics["Other"])
    
    def display_learning_words(self, words):
        """Display words for learning"""
        # Clear previous content
        for widget in self.learning_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(self.learning_frame, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_label = ctk.CTkLabel(
            scrollable_frame,
            text=f"Words for {self.profession}s ({len(words)} words)",
            font=("Inter", 20, "bold"),
            text_color=COLORS[THEME_MODE]["accent"]
        )
        header_label.pack(anchor="w", pady=(0, 20))
        
        # Instructions
        instructions_label = ctk.CTkLabel(
            scrollable_frame,
            text="Click on any word to learn its definition and add it to your vocabulary!",
            font=("Inter", 14),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        instructions_label.pack(anchor="w", pady=(0, 20))
        
        # Words grid
        words_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        words_frame.pack(fill="x")
        
        # Display words in a grid
        for i, word in enumerate(words):
            row = i // 3
            col = i % 3
            
            word_btn = ctk.CTkButton(
                words_frame,
                text=word,
                width=150,
                height=50,
                font=("Inter", 14, "bold"),
                fg_color=COLORS[THEME_MODE]["secondary_bg"],
                hover_color=COLORS[THEME_MODE]["accent"],
                command=lambda w=word: self.learn_word(w)
            )
            word_btn.grid(row=row, column=col, padx=10, pady=10)
    
    def learn_word(self, word):
        """Learn a specific word"""
        # Save to word history
        self.db.word_history(self.username, word, f"Learning - {self.profession}")
        
        # Get word definition
        definition_data = self.dictionary_api.get_word_definition(word)
        
        if definition_data:
            # Show word definition in a dialog
            from tkinter import messagebox
            
            # Create definition text
            definition_text = f"Word: {word.upper()}\n\n"
            
            if 'phonetic' in definition_data:
                definition_text += f"Pronunciation: {definition_data['phonetic']}\n\n"
            
            if 'meanings' in definition_data and definition_data['meanings']:
                meaning = definition_data['meanings'][0]  # First meaning
                if 'definitions' in meaning and meaning['definitions']:
                    definition_text += f"Definition: {meaning['definitions'][0].get('definition', 'No definition available')}\n\n"
                    
                    if 'example' in meaning['definitions'][0]:
                        definition_text += f"Example: {meaning['definitions'][0]['example']}\n\n"
            
            definition_text += f"Great choice! This word is perfect for {self.profession}s."
            
            messagebox.showinfo(f"Learn: {word}", definition_text)
        else:
            from tkinter import messagebox
            messagebox.showinfo(f"Learn: {word}", f"Word: {word.upper()}\n\nThis word has been added to your learning history!\n\nPerfect for {self.profession}s!")
    
    def show_error_message(self):
        """Show error message when no words are found"""
        error_label = ctk.CTkLabel(
            self.learning_frame,
            text="Sorry, couldn't generate words at the moment.\nPlease try again later.",
            font=("Inter", 16),
            text_color="#FF5252"
        )
        error_label.pack(expand=True)


class NotificationsPage(ctk.CTkFrame):
    """Notifications page with reading reminders"""
    
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Get current theme
        from config.settings import THEME_MODE
        self.current_theme = THEME_MODE
        
        # Notification settings
        self.notification_active = False
        self.notification_thread = None
        
        # Create notifications content
        self.create_notifications()
    
    def create_notifications(self):
        """Create the notifications page content"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="🔔 Reading Reminders",
            font=("Inter", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Main content container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Left side - Notification Settings
        left_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Settings section
        settings_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        settings_frame.pack(fill="x", padx=30, pady=30)
        
        # Section title
        settings_title = ctk.CTkLabel(
            settings_frame,
            text="⚙️ Notification Settings",
            font=("Inter", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        settings_title.pack(anchor="w", pady=(0, 20))
        
        # Notification toggle
        toggle_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        toggle_frame.pack(fill="x", pady=10)
        
        toggle_label = ctk.CTkLabel(
            toggle_frame,
            text="Enable Reading Reminders",
            font=("Inter", 16, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        toggle_label.pack(side="left")
        
        self.notification_switch = ctk.CTkSwitch(
            toggle_frame,
            text="",
            command=self.toggle_notifications,
            fg_color=COLORS[THEME_MODE]["accent"],
            progress_color=COLORS[THEME_MODE]["accent"]
        )
        self.notification_switch.pack(side="right")
        
        # Interval settings
        interval_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        interval_frame.pack(fill="x", pady=10)
        
        interval_label = ctk.CTkLabel(
            interval_frame,
            text="Reminder Interval (minutes):",
            font=("Inter", 14),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        interval_label.pack(anchor="w", pady=(0, 5))
        
        self.interval_var = ctk.StringVar(value="30")
        interval_options = ["15", "30", "60", "120", "240"]
        self.interval_dropdown = ctk.CTkOptionMenu(
            interval_frame,
            values=interval_options,
            variable=self.interval_var,
            fg_color=COLORS[THEME_MODE]["accent"],
            button_color=COLORS[THEME_MODE]["accent"],
            button_hover_color=COLORS[THEME_MODE]["accent"],
            dropdown_fg_color=COLORS[THEME_MODE]["secondary_bg"],
            dropdown_hover_color=COLORS[THEME_MODE]["accent"],
            text_color=COLORS[THEME_MODE]["text"]
        )
        self.interval_dropdown.pack(anchor="w")
        
        # Message settings
        message_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        message_frame.pack(fill="x", pady=10)
        
        message_label = ctk.CTkLabel(
            message_frame,
            text="Custom Reminder Message:",
            font=("Inter", 14),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        message_label.pack(anchor="w", pady=(0, 5))
        
        self.message_entry = ctk.CTkTextbox(
            message_frame,
            height=80,
            fg_color=COLORS[THEME_MODE]["bg"],
            text_color=COLORS[THEME_MODE]["text"],
            border_color=COLORS[THEME_MODE]["border"]
        )
        self.message_entry.pack(fill="x")
        self.message_entry.insert("1.0", "Time to learn some new words! 📚")
        
        # Test notification button
        test_btn = ctk.CTkButton(
            settings_frame,
            text="🔔 Test Notification",
            command=self.test_notification,
            fg_color=COLORS[THEME_MODE]["accent"],
            hover_color=COLORS[THEME_MODE]["accent"],
            font=("Inter", 14, "bold")
        )
        test_btn.pack(fill="x", pady=(20, 0))
        
        # Right side - Notification History
        right_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # History section
        history_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        history_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Section title
        history_title = ctk.CTkLabel(
            history_frame,
            text="📋 Notification History",
            font=("Inter", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        history_title.pack(anchor="w", pady=(0, 20))
        
        # History list
        self.history_listbox = ctk.CTkTextbox(
            history_frame,
            fg_color=COLORS[THEME_MODE]["bg"],
            text_color=COLORS[THEME_MODE]["text"],
            border_color=COLORS[THEME_MODE]["border"]
        )
        self.history_listbox.pack(fill="both", expand=True)
        
        # Add some sample history
        sample_history = [
            "🔔 Reading reminder sent - 2:30 PM",
            "🔔 Reading reminder sent - 1:00 PM", 
            "🔔 Reading reminder sent - 11:30 AM",
            "🔔 Reading reminder sent - 10:00 AM",
            "🔔 Reading reminder sent - 9:00 AM"
        ]
        
        for item in sample_history:
            self.history_listbox.insert("end", item + "\n")
    
    def toggle_notifications(self):
        """Toggle notification system"""
        if self.notification_switch.get():
            self.start_notifications()
        else:
            self.stop_notifications()
    
    def start_notifications(self):
        """Start notification system"""
        self.notification_active = True
        import threading
        self.notification_thread = threading.Thread(target=self.notification_loop, daemon=True)
        self.notification_thread.start()
    
    def stop_notifications(self):
        """Stop notification system"""
        self.notification_active = False
        if self.notification_thread:
            self.notification_thread.join(timeout=1)
    
    def notification_loop(self):
        """Notification loop in background thread"""
        import time
        from datetime import datetime
        
        while self.notification_active:
            try:
                # Get interval in minutes
                interval_minutes = int(self.interval_var.get())
                time.sleep(interval_minutes * 60)  # Convert to seconds
                
                if self.notification_active:
                    # Send notification
                    message = self.message_entry.get("1.0", "end-1c")
                    self.send_notification(message)
                    
                    # Add to history
                    current_time = datetime.now().strftime("%I:%M %p")
                    history_entry = f"🔔 Reading reminder sent - {current_time}\n"
                    self.after(0, lambda: self.add_to_history(history_entry))
                    
            except Exception as e:
                print(f"Notification error: {e}")
                break
    
    def send_notification(self, message):
        """Send system notification"""
        try:
            # Try macOS notification first
            try:
                import subprocess
                subprocess.run([
                    "osascript", "-e", 
                    f'display notification "{message}" with title "VocabLoury Reminder"'
                ], check=False)
            except:
                # Fallback to tkinter messagebox
                from tkinter import messagebox
                self.after(0, lambda: messagebox.showinfo("VocabLoury Reminder", message))
        except Exception as e:
            print(f"Notification failed: {e}")
            # Final fallback
            from tkinter import messagebox
            self.after(0, lambda: messagebox.showinfo("VocabLoury Reminder", message))
    
    def test_notification(self):
        """Test notification"""
        message = self.message_entry.get("1.0", "end-1c")
        self.send_notification(message)
    
    def add_to_history(self, entry):
        """Add entry to history"""
        self.history_listbox.insert("1.0", entry)


class TipsPage(ctk.CTkFrame):
    """Tips page with dynamic content from Google"""
    
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Get current theme
        from config.settings import THEME_MODE
        self.current_theme = THEME_MODE
        
        # Create tips content
        self.create_tips()
    
    def create_tips(self):
        """Create the tips page content"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="💡 Reading & Writing Tips",
            font=("Inter", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh Tips",
            command=self.refresh_tips,
            fg_color=COLORS[THEME_MODE]["accent"],
            hover_color=COLORS[THEME_MODE]["accent"],
            font=("Inter", 14, "bold")
        )
        refresh_btn.pack(anchor="e", pady=(0, 20))
        
        # Main content container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Tips content
        self.tips_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        self.tips_frame.pack(fill="both", expand=True)
        
        # Load initial tips
        self.load_tips()
    
    def load_tips(self):
        """Load tips content"""
        # Clear existing content
        for widget in self.tips_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        tips_content = ctk.CTkScrollableFrame(self.tips_frame, fg_color="transparent")
        tips_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Get tips from multiple sources
        tips = self.get_tips_from_sources()
        
        # Display tips
        for i, tip in enumerate(tips):
            tip_card = ctk.CTkFrame(tips_content, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=10)
            tip_card.pack(fill="x", pady=10)
            
            tip_content = ctk.CTkFrame(tip_card, fg_color="transparent")
            tip_content.pack(fill="x", padx=20, pady=15)
            
            # Tip header
            header_frame = ctk.CTkFrame(tip_content, fg_color="transparent")
            header_frame.pack(fill="x", pady=(0, 10))
            
            # Tip icon and title
            icon_title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            icon_title_frame.pack(fill="x")
            
            icon_label = ctk.CTkLabel(
                icon_title_frame,
                text=tip['icon'],
                font=("Inter", 20)
            )
            icon_label.pack(side="left")
            
            title_label = ctk.CTkLabel(
                icon_title_frame,
                text=tip['title'],
                font=("Inter", 16, "bold"),
                text_color=COLORS[THEME_MODE]["text"]
            )
            title_label.pack(side="left", padx=(10, 0))
            
            # Tip content
            content_label = ctk.CTkLabel(
                tip_content,
                text=tip['content'],
                font=("Inter", 14),
                text_color=COLORS[THEME_MODE]["text_secondary"],
                wraplength=800,
                justify="left"
            )
            content_label.pack(anchor="w")
            
            # Tip category
            category_label = ctk.CTkLabel(
                tip_content,
                text=f"Category: {tip['category']}",
                font=("Inter", 12),
                text_color=COLORS[THEME_MODE]["accent"]
            )
            category_label.pack(anchor="w", pady=(10, 0))
    
    def get_tips_from_sources(self):
        """Get tips from various sources"""
        # Curated tips with dynamic elements
        tips = [
            {
                'icon': '📚',
                'title': 'Active Reading Strategy',
                'content': 'Use the SQ3R method: Survey, Question, Read, Recite, Review. This systematic approach helps you understand and retain information more effectively.',
                'category': 'Reading Technique'
            },
            {
                'icon': '✍️',
                'title': 'Freewriting Practice',
                'content': 'Set a timer for 10-15 minutes and write continuously without stopping. Don\'t worry about grammar or structure - just let your thoughts flow freely.',
                'category': 'Writing Practice'
            },
            {
                'icon': '🧠',
                'title': 'Vocabulary Building',
                'content': 'Learn new words in context. Instead of memorizing word lists, read articles and note how words are used in sentences. This improves retention and understanding.',
                'category': 'Vocabulary'
            },
            {
                'icon': '📝',
                'title': 'Journaling for Growth',
                'content': 'Keep a daily journal to practice writing. Reflect on your day, write about your goals, or describe interesting experiences. This builds writing fluency naturally.',
                'category': 'Writing Practice'
            },
            {
                'icon': '🎯',
                'title': 'Reading Comprehension',
                'content': 'Before reading, set a purpose. Ask yourself: What do I want to learn? What questions do I have? This focused approach improves comprehension and retention.',
                'category': 'Reading Strategy'
            },
            {
                'icon': '💭',
                'title': 'Critical Thinking',
                'content': 'Question what you read. Ask: What is the author\'s main point? What evidence supports it? What are the limitations? This develops analytical skills.',
                'category': 'Critical Thinking'
            },
            {
                'icon': '🔄',
                'title': 'Spaced Repetition',
                'content': 'Review new vocabulary at increasing intervals: 1 day, 3 days, 1 week, 2 weeks. This scientifically-proven method maximizes long-term retention.',
                'category': 'Learning Technique'
            },
            {
                'icon': '📖',
                'title': 'Reading Speed',
                'content': 'Practice reading faster by using a pointer (finger or pen) to guide your eyes. This reduces regression and improves reading speed without losing comprehension.',
                'category': 'Reading Skill'
            }
        ]
        
        # Add some dynamic tips based on current time/date
        import datetime
        current_hour = datetime.datetime.now().hour
        
        if 6 <= current_hour < 12:
            tips.append({
                'icon': '🌅',
                'title': 'Morning Reading Boost',
                'content': 'Morning is the best time for complex reading. Your brain is fresh and alert, making it easier to understand difficult concepts and retain information.',
                'category': 'Timing'
            })
        elif 12 <= current_hour < 18:
            tips.append({
                'icon': '☀️',
                'title': 'Afternoon Writing',
                'content': 'Afternoon is ideal for creative writing. Your brain has warmed up and is ready for more complex thinking and creative expression.',
                'category': 'Timing'
            })
        else:
            tips.append({
                'icon': '🌙',
                'title': 'Evening Reflection',
                'content': 'Evening is perfect for reflective writing and reviewing what you\'ve learned. Use this time to journal and consolidate your daily learning.',
                'category': 'Timing'
            })
        
        return tips
    
    def refresh_tips(self):
        """Refresh tips content"""
        self.load_tips()


class ArticlesPage(ctk.CTkFrame):
    """Articles page with timer and Google articles"""
    
    def __init__(self, parent, username, db):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)
        self.username = username
        self.db = db
        
        # Get current theme
        from config.settings import THEME_MODE
        self.current_theme = THEME_MODE
        
        # Timer variables
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_thread = None
        
        # Create articles content
        self.create_articles()
    
    def create_articles(self):
        """Create the articles page content"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=40)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📰 Reading Articles",
            font=("Inter", 28, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Timer section
        timer_frame = ctk.CTkFrame(header_frame, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        timer_frame.pack(fill="x", pady=(0, 20))
        
        timer_content = ctk.CTkFrame(timer_frame, fg_color="transparent")
        timer_content.pack(fill="x", padx=30, pady=20)
        
        # Timer title
        timer_title = ctk.CTkLabel(
            timer_content,
            text="⏱️ Reading Timer",
            font=("Inter", 18, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        timer_title.pack(anchor="w", pady=(0, 15))
        
        # Timer controls
        controls_frame = ctk.CTkFrame(timer_content, fg_color="transparent")
        controls_frame.pack(fill="x")
        
        # Timer dropdown
        self.timer_var = ctk.StringVar(value="10")
        timer_dropdown = ctk.CTkOptionMenu(
            controls_frame,
            values=["10", "20", "30"],
            variable=self.timer_var,
            fg_color=COLORS[THEME_MODE]["accent"],
            button_color=COLORS[THEME_MODE]["accent"],
            button_hover_color=COLORS[THEME_MODE]["accent"],
            dropdown_fg_color=COLORS[THEME_MODE]["secondary_bg"],
            dropdown_hover_color=COLORS[THEME_MODE]["accent"],
            text_color=COLORS[THEME_MODE]["text"],
            width=100
        )
        timer_dropdown.pack(side="left", padx=(0, 15))
        
        # Start/Stop button
        self.timer_btn = ctk.CTkButton(
            controls_frame,
            text="▶️ Start Timer",
            command=self.toggle_timer,
            fg_color=COLORS[THEME_MODE]["accent"],
            hover_color=COLORS[THEME_MODE]["accent"],
            font=("Inter", 14, "bold"),
            width=120
        )
        self.timer_btn.pack(side="left", padx=(0, 15))
        
        # Timer display
        self.timer_display = ctk.CTkLabel(
            controls_frame,
            text="00:00",
            font=("Inter", 24, "bold"),
            text_color=COLORS[THEME_MODE]["accent"]
        )
        self.timer_display.pack(side="left", padx=(20, 0))
        
        # Main content container
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Articles content
        self.articles_frame = ctk.CTkFrame(main_container, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        self.articles_frame.pack(fill="both", expand=True)
        
        # Load initial articles
        self.load_articles()
    
    def toggle_timer(self):
        """Toggle timer start/stop"""
        if not self.timer_running:
            self.start_timer()
        else:
            self.stop_timer()
    
    def start_timer(self):
        """Start the reading timer"""
        self.timer_running = True
        self.timer_seconds = int(self.timer_var.get()) * 60  # Convert minutes to seconds
        self.timer_btn.configure(text="⏹️ Stop Timer")
        
        # Start timer thread
        import threading
        self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        self.timer_thread.start()
    
    def stop_timer(self):
        """Stop the reading timer"""
        self.timer_running = False
        self.timer_btn.configure(text="▶️ Start Timer")
        self.timer_display.configure(text="00:00")
    
    def timer_loop(self):
        """Timer loop in background thread"""
        import time
        
        while self.timer_running and self.timer_seconds > 0:
            # Update display
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.after(0, lambda: self.timer_display.configure(text=time_str))
            
            time.sleep(1)
            self.timer_seconds -= 1
        
        # Timer finished
        if self.timer_running:
            self.after(0, self.timer_finished)
    
    def timer_finished(self):
        """Handle timer completion"""
        self.timer_running = False
        self.timer_btn.configure(text="▶️ Start Timer")
        self.timer_display.configure(text="00:00")
        
        # Show completion notification
        from tkinter import messagebox
        messagebox.showinfo("Timer Complete!", "Great job! You've completed your reading session! 🎉")
    
    def load_articles(self):
        """Load articles content"""
        # Clear existing content
        for widget in self.articles_frame.winfo_children():
            widget.destroy()
        
        # Create scrollable frame
        articles_content = ctk.CTkScrollableFrame(self.articles_frame, fg_color="transparent")
        articles_content.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Header
        header_label = ctk.CTkLabel(
            articles_content,
            text="📚 Educational Articles",
            font=("Inter", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"]
        )
        header_label.pack(anchor="w", pady=(0, 20))
        
        # Get articles from various sources
        articles = self.get_articles_from_sources()
        
        # Display articles
        for i, article in enumerate(articles):
            article_card = ctk.CTkFrame(articles_content, fg_color=COLORS[THEME_MODE]["bg"], corner_radius=10)
            article_card.pack(fill="x", pady=10)
            
            article_content = ctk.CTkFrame(article_card, fg_color="transparent")
            article_content.pack(fill="x", padx=20, pady=15)
            
            # Article header
            header_frame = ctk.CTkFrame(article_content, fg_color="transparent")
            header_frame.pack(fill="x", pady=(0, 10))
            
            # Article title
            title_label = ctk.CTkLabel(
                header_frame,
                text=article['title'],
                font=("Inter", 16, "bold"),
                text_color=COLORS[THEME_MODE]["text"],
                wraplength=800,
                justify="left"
            )
            title_label.pack(anchor="w")
            
            # Article meta info
            meta_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            meta_frame.pack(fill="x", pady=(5, 0))
            
            category_label = ctk.CTkLabel(
                meta_frame,
                text=f"📂 {article['category']}",
                font=("Inter", 12),
                text_color=COLORS[THEME_MODE]["accent"]
            )
            category_label.pack(side="left")
            
            read_time_label = ctk.CTkLabel(
                meta_frame,
                text=f"⏱️ {article['read_time']}",
                font=("Inter", 12),
                text_color=COLORS[THEME_MODE]["text_secondary"]
            )
            read_time_label.pack(side="right")
            
            # Article summary
            summary_label = ctk.CTkLabel(
                article_content,
                text=article['summary'],
                font=("Inter", 14),
                text_color=COLORS[THEME_MODE]["text_secondary"],
                wraplength=800,
                justify="left"
            )
            summary_label.pack(anchor="w", pady=(0, 10))
            
            # Read button
            read_btn = ctk.CTkButton(
                article_content,
                text="📖 Read Article",
                command=lambda article_data=article: self.show_article_content(article_data),
                fg_color=COLORS[THEME_MODE]["accent"],
                hover_color=COLORS[THEME_MODE]["accent"],
                font=("Inter", 12, "bold"),
                width=120
            )
            read_btn.pack(anchor="w")
    
    def get_articles_from_sources(self):
        """Get articles from various educational sources"""
        # Curated educational articles with full content
        articles = [
            {
                'title': 'The Science of Reading: How Your Brain Processes Text',
                'category': 'Education',
                'read_time': '5 min read',
                'summary': 'Discover the fascinating neuroscience behind reading comprehension and how your brain processes written language.',
                'full_content': '''Introduction

Reading is one of the most complex cognitive processes humans engage in. When you read, your brain performs an incredible symphony of neural activities that transform symbols on a page into meaningful understanding. This article explores the fascinating science behind how your brain processes text.

The Visual Processing System

When you look at text, light reflected from the page enters your eyes and hits the retina. Specialized cells called photoreceptors convert this light into electrical signals that travel through the optic nerve to your brain's visual cortex. Here, the brain begins the complex task of recognizing letters and words.

The brain processes text in a hierarchical manner:
• Individual letters are recognized first
• Letters are combined into words
• Words are combined into phrases and sentences
• Meaning is extracted from the complete text

Word Recognition and Language Processing

Your brain has specialized areas for language processing. The left hemisphere contains key language centers including:
• Broca's area (speech production)
• Wernicke's area (language comprehension)
• The angular gyrus (reading and writing)

When you read a word, your brain doesn't just recognize its visual form—it also activates:
• Phonological representations (how the word sounds)
• Semantic representations (what the word means)
• Syntactic information (how the word functions in sentences)

Reading Comprehension

True reading comprehension involves more than just recognizing words. Your brain must:
1. Parse sentence structure
2. Connect ideas across sentences
3. Make inferences
4. Integrate new information with existing knowledge
5. Monitor understanding and detect confusion

The Role of Working Memory

Working memory plays a crucial role in reading comprehension. It allows you to:
• Hold information in mind while processing new text
• Connect ideas across sentences and paragraphs
• Make inferences and predictions
• Monitor your understanding

Conclusion

The science of reading reveals the incredible complexity of this seemingly simple activity. Understanding these processes can help you become a more effective reader by optimizing how you engage with text and manage your cognitive resources.'''
            },
            {
                'title': 'Vocabulary Building Strategies for Language Learners',
                'category': 'Language Learning',
                'read_time': '7 min read',
                'summary': 'Learn effective techniques to expand your vocabulary and improve your language skills through proven methods.',
                'full_content': '''Introduction

Building a strong vocabulary is essential for effective communication and language mastery. Whether you're learning a new language or expanding your native language skills, these proven strategies will help you acquire and retain new words more effectively.

Contextual Learning

One of the most effective ways to learn new vocabulary is through context. Instead of memorizing isolated word lists, learn words as they appear in sentences, stories, or conversations. This approach helps you understand:
• How words are used in real situations
• Common collocations and word partnerships
• Appropriate register and tone
• Cultural nuances and connotations

Spaced Repetition System

Spaced repetition is a scientifically proven method for long-term retention. The technique involves reviewing words at increasing intervals:
• Day 1: Learn new words
• Day 2: Review
• Day 4: Review again
• Day 8: Review
• Day 16: Review
• Continue with longer intervals

This method takes advantage of the "forgetting curve" and helps move information from short-term to long-term memory.

Active Usage

Simply recognizing words isn't enough—you need to actively use them. Try these techniques:
• Write sentences using new words
• Use words in conversations
• Create stories or paragraphs incorporating new vocabulary
• Practice with flashcards that require you to produce the word, not just recognize it

Word Families and Etymology

Understanding word families and etymology can exponentially expand your vocabulary:
• Learn root words, prefixes, and suffixes
• Study how words are formed and related
• Understand the history and origin of words
• Recognize patterns in word formation

Reading Extensively

Reading is one of the most powerful vocabulary-building activities:
• Read materials slightly above your current level
• Don't stop to look up every unknown word
• Focus on understanding the overall meaning
• Keep a vocabulary journal for interesting words
• Re-read texts to reinforce learning

Conclusion

Building vocabulary is a lifelong process that requires consistent effort and the right strategies. By combining contextual learning, spaced repetition, active usage, and extensive reading, you can significantly expand your vocabulary and improve your language skills.'''
            },
            {
                'title': 'The Art of Critical Reading: Analyzing Texts Effectively',
                'category': 'Reading Skills',
                'read_time': '6 min read',
                'summary': 'Master the skills of critical reading and learn how to analyze texts for deeper understanding and insight.',
                'full_content': '''Introduction

Critical reading goes beyond simply understanding what a text says—it involves analyzing, evaluating, and questioning the content to develop deeper insights and make informed judgments. This skill is essential for academic success, professional development, and informed citizenship.

What is Critical Reading?

Critical reading is an active process that involves:
• Analyzing the author's arguments and evidence
• Evaluating the credibility of sources
• Identifying biases and assumptions
• Making connections between ideas
• Forming your own informed opinions

The Critical Reading Process

1. Preview and Predict
Before diving into the text, take time to:
• Read the title, headings, and subheadings
• Look at any images, charts, or graphs
• Read the introduction and conclusion
• Make predictions about the content and arguments

2. Active Reading
While reading, engage actively with the text:
• Ask questions about the content
• Make notes and annotations
• Identify key arguments and supporting evidence
• Look for logical connections and transitions
• Note any confusing or unclear passages

3. Analysis and Evaluation
After reading, analyze the text by considering:
• What is the author's main argument or purpose?
• What evidence supports the argument?
• Are the sources credible and relevant?
• What assumptions does the author make?
• Are there any logical fallacies or weaknesses?

Questioning Techniques

Develop the habit of asking critical questions:
• Who is the author and what are their credentials?
• When was this written and how might that affect the content?
• What is the author's perspective or bias?
• What evidence is presented and is it sufficient?
• What alternative viewpoints exist?
• How does this relate to other things you know?

Identifying Bias and Assumptions

Critical readers learn to recognize:
• Author bias and perspective
• Unstated assumptions
• Loaded language and emotional appeals
• Cherry-picked evidence
• Oversimplification of complex issues

Making Connections

Critical reading involves connecting ideas:
• How does this relate to other texts you've read?
• What are the broader implications of the arguments?
• How does this fit into larger debates or discussions?
• What questions does this raise for further investigation?

Conclusion

Critical reading is a skill that develops with practice. By approaching texts with curiosity, skepticism, and analytical thinking, you can become a more informed and thoughtful reader. This skill will serve you well in academic, professional, and personal contexts throughout your life.'''
            },
            {
                'title': 'Writing Techniques: From First Draft to Final Copy',
                'category': 'Writing',
                'read_time': '8 min read',
                'summary': 'Explore the writing process from initial brainstorming to polished final drafts with practical tips and techniques.',
                'full_content': '''Introduction

Writing is a process, not a single event. The journey from initial idea to polished final draft involves multiple stages, each with its own techniques and strategies. Understanding and mastering this process can transform your writing from good to exceptional.

The Writing Process Overview

Effective writing typically follows these stages:
1. Prewriting and Planning
2. Drafting
3. Revising
4. Editing
5. Proofreading

Each stage serves a specific purpose and requires different skills and approaches.

Stage 1: Prewriting and Planning

Before you write a single word, invest time in planning:
• Brainstorm ideas and topics
• Research and gather information
• Create outlines or mind maps
• Identify your audience and purpose
• Establish your main argument or thesis

Planning Techniques:
• Freewriting: Write continuously for a set time without stopping
• Clustering: Create visual maps of related ideas
• Questioning: Use the 5 W's (who, what, when, where, why)
• Outlining: Create structured plans with main points and subpoints

Stage 2: Drafting

The drafting stage is about getting your ideas down on paper:
• Don't worry about perfection—focus on content
• Write quickly and continuously
• Use your outline as a guide but be flexible
• Don't stop to edit or perfect sentences
• Aim for a complete first draft

Drafting Tips:
• Set aside dedicated writing time
• Eliminate distractions
• Write in a comfortable environment
• Don't judge your writing during this stage
• Keep your audience in mind

Stage 3: Revising

Revision focuses on improving content, organization, and clarity:
• Review your overall structure and flow
• Check that your argument is clear and well-supported
• Ensure all paragraphs support your main thesis
• Look for gaps in logic or evidence
• Consider your audience's needs and expectations

Revision Questions:
• Does the introduction clearly state your purpose?
• Is your argument logical and well-supported?
• Are your paragraphs well-organized?
• Does the conclusion effectively wrap up your ideas?
• Is the tone appropriate for your audience?

Stage 4: Editing

Editing focuses on sentence-level improvements:
• Vary sentence structure and length
• Use active voice when possible
• Eliminate wordiness and redundancy
• Improve word choice and precision
• Ensure smooth transitions between ideas

Editing Techniques:
• Read your work aloud
• Use grammar and style checkers
• Focus on one type of error at a time
• Take breaks between editing sessions
• Get feedback from others

Stage 5: Proofreading

Proofreading is the final stage, focusing on surface errors:
• Check spelling and grammar
• Verify punctuation and capitalization
• Ensure consistent formatting
• Check for typos and missing words
• Verify citations and references

Proofreading Tips:
• Read slowly and carefully
• Use spell-check but don't rely on it completely
• Read backwards to catch spelling errors
• Print out your work for final review
• Have someone else proofread if possible

Common Writing Challenges and Solutions

Writer's Block:
• Freewrite for 10-15 minutes
• Change your writing environment
• Start with a different section
• Talk through your ideas with someone

Perfectionism:
• Remember that first drafts are meant to be imperfect
• Focus on getting ideas down first
• Save perfectionism for later stages
• Set realistic goals and deadlines

Conclusion

Mastering the writing process takes time and practice, but understanding each stage and its purpose will help you become a more effective and confident writer. Remember that good writing is rewriting—most professional writers go through multiple drafts before producing their final work.'''
            },
            {
                'title': 'Memory Techniques for Better Learning Retention',
                'category': 'Learning',
                'read_time': '6 min read',
                'summary': 'Discover memory techniques and strategies to improve your learning retention and recall abilities.',
                'full_content': '''Introduction

Memory is the foundation of learning. Without the ability to retain and recall information, all our efforts to acquire knowledge would be in vain. Fortunately, memory is not a fixed ability—it can be improved through understanding how it works and applying proven techniques.

How Memory Works

Memory involves three main processes:
1. Encoding: Converting information into a form that can be stored
2. Storage: Maintaining information over time
3. Retrieval: Accessing stored information when needed

Understanding these processes helps us optimize our learning strategies.

The Forgetting Curve

Hermann Ebbinghaus discovered that we forget information rapidly without reinforcement:
• We forget 50% of new information within an hour
• We forget 70% within 24 hours
• We forget 90% within a week

This curve shows why review and repetition are essential for long-term retention.

Effective Memory Techniques

1. Spaced Repetition
Review information at increasing intervals:
• Day 1: Learn new material
• Day 2: Review
• Day 4: Review
• Day 8: Review
• Day 16: Review
• Continue with longer intervals

2. Active Recall
Instead of just re-reading, actively test yourself:
• Cover your notes and try to recall key points
• Use flashcards
• Explain concepts to someone else
• Take practice tests
• Teach the material to others

3. Elaborative Interrogation
Ask yourself "why" and "how" questions:
• Why does this concept work this way?
• How does this relate to what I already know?
• What are the implications of this information?
• How can I apply this in different situations?

4. Dual Coding
Combine verbal and visual information:
• Create mind maps and diagrams
• Use images and symbols
• Draw pictures to represent concepts
• Watch videos and read text on the same topic
• Use color coding in your notes

5. Chunking
Break large amounts of information into smaller, manageable pieces:
• Group related information together
• Create acronyms or mnemonics
• Organize information hierarchically
• Use patterns and structures

6. Method of Loci (Memory Palace)
Associate information with familiar locations:
• Choose a familiar place (your home, school, etc.)
• Create a mental route through the location
• Associate each piece of information with a specific location
• Walk through the route to recall information

7. Story Method
Create stories that incorporate the information you want to remember:
• Make the story vivid and memorable
• Include all the key information
• Use characters, actions, and settings
• Make it personal and emotional

8. Acronyms and Mnemonics
Create memory aids using:
• First letters of words (ROY G. BIV for colors of the rainbow)
• Rhymes and songs
• Acronyms (HOMES for the Great Lakes)
• Visual associations

Optimizing Your Study Environment

Create conditions that support memory:
• Study in a quiet, distraction-free environment
• Use consistent study locations
• Take regular breaks (Pomodoro Technique)
• Get adequate sleep
• Exercise regularly
• Maintain a healthy diet

The Role of Sleep in Memory

Sleep is crucial for memory consolidation:
• Information is transferred from short-term to long-term memory during sleep
• Different stages of sleep consolidate different types of memories
• Lack of sleep significantly impairs learning and memory
• Aim for 7-9 hours of quality sleep per night

Emotional and Social Factors

Memory is enhanced by:
• Emotional engagement with the material
• Social interaction and discussion
• Personal relevance and interest
• Positive emotions and motivation
• Stress management

Conclusion

Improving your memory is a skill that can be developed with practice and the right techniques. By understanding how memory works and applying these proven strategies, you can significantly enhance your learning retention and recall abilities. Remember that different techniques work better for different types of information and different learning styles, so experiment to find what works best for you.'''
            },
            {
                'title': 'Digital Literacy in the Modern World',
                'category': 'Technology',
                'read_time': '5 min read',
                'summary': 'Understand the importance of digital literacy and how to navigate the digital landscape effectively.',
                'full_content': '''Introduction

In our increasingly digital world, digital literacy has become as essential as traditional literacy. It encompasses the skills, knowledge, and attitudes needed to effectively use digital technologies for learning, working, and participating in society.

What is Digital Literacy?

Digital literacy involves:
• Technical skills to use digital devices and software
• Critical thinking to evaluate digital information
• Communication skills for digital environments
• Safety and security awareness
• Ethical understanding of digital citizenship

Core Components of Digital Literacy

1. Technical Skills
Basic technical competencies include:
• Using computers, tablets, and smartphones
• Navigating operating systems and software
• Understanding file management
• Using productivity tools (word processors, spreadsheets, presentations)
• Basic troubleshooting and problem-solving

2. Information Literacy
The ability to find, evaluate, and use digital information:
• Effective search strategies
• Evaluating source credibility
• Understanding different types of online content
• Recognizing bias and misinformation
• Citing digital sources properly

3. Communication and Collaboration
Skills for digital communication:
• Email etiquette and professional communication
• Social media awareness and responsibility
• Online collaboration tools
• Video conferencing and virtual meetings
• Digital presentation skills

4. Digital Security and Privacy
Protecting yourself and your information online:
• Creating strong passwords
• Recognizing phishing and scams
• Understanding privacy settings
• Safe browsing practices
• Data protection and backup strategies

5. Digital Citizenship
Ethical behavior in digital environments:
• Respecting others online
• Understanding digital rights and responsibilities
• Combating cyberbullying
• Respecting intellectual property
• Contributing positively to online communities

The Importance of Digital Literacy

Digital literacy is crucial because:
• Most jobs require digital skills
• Education increasingly relies on digital tools
• Civic participation happens online
• Social connections are maintained digitally
• Access to services and information is primarily digital

Developing Digital Literacy Skills

1. Start with the Basics
• Learn fundamental computer operations
• Practice with common software applications
• Explore different types of digital devices
• Build confidence through regular use

2. Practice Critical Thinking
• Question information found online
• Verify facts from multiple sources
• Understand how algorithms affect what you see
• Recognize the difference between opinion and fact

3. Stay Updated
• Technology changes rapidly
• Follow reputable tech news sources
• Participate in online learning communities
• Take advantage of free online courses

4. Learn by Doing
• Experiment with new tools and platforms
• Join online communities related to your interests
• Create digital content (blogs, videos, presentations)
• Practice digital communication skills

5. Seek Help When Needed
• Don't be afraid to ask questions
• Use help documentation and tutorials
• Join online forums and communities
• Take advantage of library and community resources

Common Digital Literacy Challenges

Information Overload:
• Learn to filter and prioritize information
• Use tools to organize digital content
• Develop strategies for managing digital distractions
• Practice focused attention and deep work

Privacy Concerns:
• Understand what information you're sharing
• Regularly review privacy settings
• Be cautious about personal information online
• Use privacy-focused tools when possible

Technology Anxiety:
• Start with familiar tools and gradually expand
• Practice regularly to build confidence
• Remember that everyone learns at their own pace
• Focus on practical applications that interest you

The Future of Digital Literacy

As technology continues to evolve, digital literacy will need to adapt:
• Artificial intelligence and machine learning
• Virtual and augmented reality
• Internet of Things (IoT) devices
• Blockchain and cryptocurrency
• Advanced data analytics

Conclusion

Digital literacy is not just about using technology—it's about using it wisely, safely, and effectively. In our digital age, these skills are essential for success in education, work, and life. By developing your digital literacy skills, you're not just learning to use tools; you're preparing yourself to thrive in an increasingly connected world.'''
            },
            {
                'title': 'The Psychology of Learning: How We Acquire Knowledge',
                'category': 'Psychology',
                'read_time': '7 min read',
                'summary': 'Explore the psychological principles behind learning and how understanding them can improve your study habits.',
                'full_content': '''Introduction

Learning is one of the most fundamental human activities, yet it's often taken for granted. Understanding the psychological principles behind how we acquire, process, and retain knowledge can significantly improve our learning effectiveness and efficiency.

The Science of Learning

Learning psychology examines how people acquire, process, and retain information. Key areas include:
• Cognitive processes involved in learning
• Factors that influence learning effectiveness
• Individual differences in learning styles
• The role of motivation and emotion
• Memory and retention strategies

Cognitive Load Theory

Developed by John Sweller, this theory explains how our working memory processes information:
• Intrinsic load: The inherent difficulty of the material
• Extraneous load: How the information is presented
• Germane load: The effort required to create long-term memories

Implications for learning:
• Break complex information into smaller chunks
• Eliminate unnecessary distractions
• Use visual aids and examples
• Allow time for processing and reflection

Learning Styles and Preferences

While the concept of distinct learning styles is debated, people do have preferences for how they process information:
• Visual learners: Prefer images, diagrams, and spatial information
• Auditory learners: Learn best through listening and discussion
• Kinesthetic learners: Learn through movement and hands-on activities
• Reading/writing learners: Prefer text-based materials

Effective strategies:
• Use multiple modalities when possible
• Adapt your study methods to your preferences
• Don't limit yourself to one approach
• Experiment with different techniques

The Role of Motivation

Motivation is crucial for learning success:
• Intrinsic motivation: Learning for its own sake
• Extrinsic motivation: Learning for external rewards
• Self-determination theory: Autonomy, competence, and relatedness
• Goal-setting theory: Specific, challenging, and achievable goals

Ways to increase motivation:
• Connect learning to personal interests and goals
• Set clear, achievable objectives
• Celebrate progress and achievements
• Find social support and accountability
• Make learning relevant and meaningful

Memory and Retention

Understanding how memory works can improve retention:
• Sensory memory: Brief storage of sensory information
• Short-term memory: Limited capacity, temporary storage
• Long-term memory: Unlimited capacity, permanent storage
• Working memory: Active processing of information

Memory improvement strategies:
• Use spaced repetition
• Practice active recall
• Create meaningful associations
• Use multiple senses
• Get adequate sleep

The Testing Effect

Research shows that testing improves learning more than re-reading:
• Retrieval practice strengthens memory
• Testing identifies knowledge gaps
• Frequent testing improves long-term retention
• Self-testing is as effective as formal tests

Practical applications:
• Use flashcards regularly
• Take practice tests
• Quiz yourself on material
• Explain concepts to others
• Use the Feynman technique

Metacognition: Thinking About Thinking

Metacognition involves awareness and control of your own learning:
• Planning: Setting goals and strategies
• Monitoring: Tracking your understanding
• Evaluating: Assessing your performance
• Regulating: Adjusting your approach

Developing metacognitive skills:
• Reflect on your learning process
• Monitor your comprehension
• Use self-questioning techniques
• Keep a learning journal
• Seek feedback from others

The Role of Emotion in Learning

Emotions significantly impact learning:
• Positive emotions enhance learning and memory
• Stress and anxiety can impair performance
• Interest and curiosity drive engagement
• Social emotions influence motivation

Managing emotions for better learning:
• Create a positive learning environment
• Manage stress and anxiety
• Cultivate curiosity and interest
• Build confidence through success
• Use relaxation techniques

Social Learning

Learning is often a social process:
• Collaboration enhances understanding
• Discussion clarifies thinking
• Teaching others improves your own learning
• Social support increases motivation
• Peer feedback provides valuable perspectives

Strategies for social learning:
• Form study groups
• Participate in discussions
• Teach others what you've learned
• Seek feedback from peers and mentors
• Join learning communities

Individual Differences

People learn differently due to various factors:
• Prior knowledge and experience
• Cognitive abilities and processing speed
• Attention and focus abilities
• Cultural background and values
• Personality traits and preferences

Adapting to individual differences:
• Assess your strengths and weaknesses
• Use strategies that work for you
• Don't compare yourself to others
• Seek help when needed
• Be patient with your progress

Conclusion

Understanding the psychology of learning can transform how you approach education and skill development. By applying these principles—managing cognitive load, using effective memory strategies, staying motivated, and developing metacognitive awareness—you can become a more effective and efficient learner. Remember that learning is a skill that can be improved with practice and the right strategies.'''
            },
            {
                'title': 'Speed Reading: Techniques and Benefits',
                'category': 'Reading Skills',
                'read_time': '6 min read',
                'summary': 'Learn speed reading techniques that can help you read faster while maintaining comprehension.',
                'full_content': '''Introduction

Speed reading is a collection of techniques designed to increase reading speed while maintaining or improving comprehension. In our information-rich world, the ability to process text quickly and efficiently is a valuable skill that can save time and increase productivity.

What is Speed Reading?

Speed reading involves:
• Reading at speeds significantly faster than normal (typically 200-400 words per minute)
• Maintaining comprehension of the material
• Using specific techniques to optimize reading efficiency
• Adapting speed based on material complexity and purpose

The average reading speed is about 200-250 words per minute, while speed readers can achieve 400-1000+ words per minute.

Core Speed Reading Techniques

1. Eliminate Subvocalization
Subvocalization is the habit of "hearing" words in your head as you read:
• This limits reading speed to speaking speed
• Practice reading without "saying" words internally
• Use techniques like humming or counting to break the habit
• Focus on visual recognition of words and phrases

2. Reduce Fixations
Fixations are the points where your eyes stop while reading:
• Average readers have 3-4 fixations per line
• Speed readers aim for 1-2 fixations per line
• Practice taking in more words per fixation
• Use peripheral vision to see more text at once

3. Eliminate Regression
Regression is the habit of going back to re-read text:
• This significantly slows reading speed
• Trust your comprehension and keep moving forward
• Use a pointer or guide to maintain forward momentum
• Only go back if you truly don't understand something

4. Expand Your Vision Span
Train your eyes to take in more text at once:
• Practice reading groups of words instead of individual words
• Use exercises to expand your peripheral vision
• Focus on reading phrases and clauses as units
• Gradually increase the amount of text you can process at once

5. Use a Pointer or Guide
Using a finger, pen, or pointer can help:
• Maintain consistent reading pace
• Reduce fixations and regressions
• Keep your eyes focused and moving forward
• Provide a visual guide for your reading

Advanced Speed Reading Techniques

1. Skimming and Scanning
• Skimming: Quickly reading to get the main ideas
• Scanning: Looking for specific information
• Use these techniques when you don't need complete comprehension
• Practice identifying key information quickly

2. Previewing
Before reading in detail:
• Read the title, headings, and subheadings
• Look at any images, charts, or graphs
• Read the introduction and conclusion
• Get an overview of the structure and main points

3. Chunking
Group words together for faster processing:
• Read phrases and clauses as units
• Practice recognizing common word patterns
• Focus on meaning rather than individual words
• Use punctuation as natural break points

4. Meta Guiding
Use your hand or a pointer to guide your eyes:
• Move your pointer smoothly across the line
• Use different patterns (straight line, S-curve, or zigzag)
• Practice maintaining a steady pace
• Gradually increase your speed

Benefits of Speed Reading

1. Time Efficiency
• Read more material in less time
• Process information faster
• Increase productivity in academic and professional settings
• Have more time for other activities

2. Improved Focus
• Speed reading requires concentration
• Reduces mind-wandering and distractions
• Develops better attention skills
• Creates a more active reading experience

3. Better Comprehension
• Forces you to focus on main ideas
• Reduces the tendency to get lost in details
• Improves pattern recognition
• Develops better reading strategies

4. Increased Confidence
• Mastery of a valuable skill
• Reduced anxiety about reading assignments
• Greater sense of control over learning
• Improved academic and professional performance

Limitations and Considerations

Speed reading isn't appropriate for all situations:
• Complex technical material may require slower, more careful reading
• Literature and poetry often benefit from slower, more thoughtful reading
• Some people may find it difficult to maintain comprehension at high speeds
• It takes time and practice to develop speed reading skills

When to Use Speed Reading

Speed reading is most effective for:
• News articles and blog posts
• General informational texts
• Reviewing familiar material
• Getting an overview of a topic
• Processing large amounts of information quickly

When to Read Slowly

Take your time with:
• Complex technical or scientific material
• Literature and creative writing
• Material you need to memorize
• Important documents or contracts
• Material that requires deep analysis

Developing Speed Reading Skills

1. Start with Easy Material
• Begin with simple, familiar texts
• Gradually increase complexity
• Practice with different types of content
• Build confidence before tackling difficult material

2. Practice Regularly
• Dedicate time each day to speed reading practice
• Use a variety of materials
• Track your progress
• Be patient with the learning process

3. Measure Your Progress
• Time your reading sessions
• Test your comprehension
• Keep a reading log
• Set realistic goals for improvement

4. Use Technology
• Speed reading apps and software
• Online courses and tutorials
• Reading speed tests
• Digital tools for practice

Conclusion

Speed reading is a valuable skill that can significantly improve your reading efficiency and productivity. While it requires practice and isn't suitable for all types of reading, the techniques can help you process information faster and more effectively. Remember that the goal is not just speed, but efficient reading that maintains comprehension and serves your learning objectives.'''
            }
        ]
        
        return articles
    
    def show_article_content(self, article):
        """Show full article content within the app"""
        # Create a new window for article content
        article_window = ctk.CTkToplevel(self)
        article_window.title(f"📰 {article['title']}")
        article_window.geometry("1000x700")
        article_window.configure(fg_color=COLORS[THEME_MODE]["bg"])
        
        # Make window modal
        article_window.transient(self)
        article_window.grab_set()
        
        # Header frame
        header_frame = ctk.CTkFrame(article_window, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # Article title
        title_label = ctk.CTkLabel(
            header_frame,
            text=article['title'],
            font=("Inter", 20, "bold"),
            text_color=COLORS[THEME_MODE]["text"],
            wraplength=900,
            justify="center"
        )
        title_label.pack(pady=20)
        
        # Article meta info
        meta_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        meta_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        category_label = ctk.CTkLabel(
            meta_frame,
            text=f"📂 {article['category']}",
            font=("Inter", 14, "bold"),
            text_color=COLORS[THEME_MODE]["accent"]
        )
        category_label.pack(side="left")
        
        read_time_label = ctk.CTkLabel(
            meta_frame,
            text=f"⏱️ {article['read_time']}",
            font=("Inter", 14),
            text_color=COLORS[THEME_MODE]["text_secondary"]
        )
        read_time_label.pack(side="right")
        
        # Content frame
        content_frame = ctk.CTkScrollableFrame(article_window, fg_color=COLORS[THEME_MODE]["secondary_bg"], corner_radius=15)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Article content
        content_text = ctk.CTkTextbox(
            content_frame,
            fg_color=COLORS[THEME_MODE]["bg"],
            text_color=COLORS[THEME_MODE]["text"],
            border_color=COLORS[THEME_MODE]["border"],
            font=("Inter", 14),
            wrap="word"
        )
        content_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Insert article content
        content_text.insert("1.0", article['full_content'])
        content_text.configure(state="disabled")  # Make read-only
        
        # Close button
        close_btn = ctk.CTkButton(
            article_window,
            text="✕ Close",
            command=article_window.destroy,
            fg_color="#FF5252",
            hover_color="#FF5252",
            font=("Inter", 14, "bold"),
            width=100
        )
        close_btn.pack(pady=20)
