#!/usr/bin/env python3
"""
VocabLoury Launcher - Easy way to start the application
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    print("🎯 VocabLoury - Professional Dictionary & Learning App")
    print("=" * 50)
    print("Choose your preferred interface:")
    print("1. 🖥️  Desktop Application (CustomTkinter)")
    print("2. 🌐 Web Interface (Modern HTML/CSS/JS)")
    print("3. 📱 Web Interface (Custom Port)")
    print("4. 🔔 Notification Only")
    print("5. ❌ Exit")
    print("=" * 50)
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting Desktop Application...")
                subprocess.run([sys.executable, "main.py"])
                break
                
            elif choice == "2":
                print("\n🌐 Starting Web Interface...")
                subprocess.run([sys.executable, "main.py", "--web"])
                break
                
            elif choice == "3":
                port = input("Enter port number (default 8000): ").strip()
                if not port:
                    port = "8000"
                print(f"\n🌐 Starting Web Interface on port {port}...")
                subprocess.run([sys.executable, "main.py", "--web", "--port", port])
                break
                
            elif choice == "4":
                username = input("Enter username for notification: ").strip()
                if username:
                    print(f"\n🔔 Showing notification for {username}...")
                    subprocess.run([sys.executable, "main.py", "--notify", username])
                else:
                    print("❌ Username is required for notifications")
                break
                
            elif choice == "5":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
