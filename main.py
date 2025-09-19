"""
Main entry point for VocabLoury application
"""

import sys
import os
import argparse

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controllers.auth_controller import AuthenticationApp
from config.settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT


def handle_command_line():
    """Handle command line arguments"""
    parser = argparse.ArgumentParser(description="VocabLoury - Professional Dictionary & Learning App")
    parser.add_argument("--notify", help="Username to show notification")
    parser.add_argument("--web", action="store_true", help="Launch web interface")
    parser.add_argument("--port", type=int, default=8000, help="Port for web server (default: 8000)")
    args = parser.parse_args()
    
    if args.notify:
        # Show notification
        from views.notifications import CustomNotification
        notification = CustomNotification(args.notify, "Time to learn a new word!")
        notification.mainloop()
    elif args.web:
        # Launch web interface
        from utils.web_server import serve_static_files
        print("🚀 Starting VocabLoury Web Interface...")
        print(f"📱 Web interface will be available at: http://localhost:{args.port}")
        print("💡 The web interface provides a modern, responsive UI with professional styling")
        print("🎨 Features multiple themes, animations, and enhanced user experience")
        print("⏹️  Press Ctrl+C to stop the server")
        
        try:
            serve_static_files(args.port, open_browser=True)
            # Keep the main thread alive
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Web server stopped. Goodbye!")
    else:
        # Launch desktop application
        print("🖥️  Starting VocabLoury Desktop Application...")
        app = AuthenticationApp()
        app.run()


if __name__ == "__main__":
    handle_command_line()
