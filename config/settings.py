"""
Configuration settings for VocabLoury application
"""

# Theme settings
THEME_MODE = "dark"

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
ANIMATION_INTERVAL = 50  # milliseconds
PARTICLE_COUNT = 20

# Window settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
WINDOW_TITLE = "VocabLoury - Dictionary & Learning App"
