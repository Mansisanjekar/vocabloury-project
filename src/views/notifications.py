"""
Notification system for VocabLoury application
"""

import tkinter as tk


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
