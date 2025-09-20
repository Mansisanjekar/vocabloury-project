"""
Configuration settings for VocabLoury application
"""

# Theme settings
THEME_MODE = "dark"

# Color schemes
COLORS = {
    "dark": {
        "bg": "#000000",  # Pure black background
        "secondary_bg": "#1a1a1a",  # Dark gray secondary background
        "accent": "#1f538d",  # Professional blue accent
        "text": "#ffffff",  # Pure white text
        "text_secondary": "#cccccc",  # Light gray secondary text
        "border": "#333333"  # Dark gray borders
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

# Profession to topic mapping
PROFESSION_TO_TOPIC = {
    "Student": "education",
    "Entrepreneur": "money",
    "Scientist": "science",
    "Musician": "music",
    "Writer": "writing"
}

# API settings
DICTIONARY_API_BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en"
DATAMUSE_API_BASE_URL = "https://api.datamuse.com/words"

# Database settings
DATABASE_NAME = "authentication.db"

# Animation settings
ANIMATION_INTERVAL = 30  # milliseconds (faster animation)
PARTICLE_COUNT = 30  # More particles

# Window settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
WINDOW_TITLE = "VocabLoury - Dictionary & Learning App"
