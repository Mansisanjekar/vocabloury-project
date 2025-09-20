"""
Main entry point for VocabLoury Desktop Application
"""

import sys
import os
import customtkinter as ctk

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controllers.auth_controller import AuthenticationApp
from config.settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, THEME_MODE


def main():
    """Main application entry point"""
    print("🖥️  Starting VocabLoury Desktop Application...")
    print("📚 Professional Dictionary & Learning App")
    print("🎨 Modern UI with Black Theme")
    print("✨ Enhanced Animations & Professional Design")
    
    # Set appearance mode
    ctk.set_appearance_mode(THEME_MODE)
    ctk.set_default_color_theme("blue")
    
    # Create and run the application
    app = AuthenticationApp()
    app.run()


if __name__ == "__main__":
    main()
