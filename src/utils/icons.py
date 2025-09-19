"""
Professional icon system for VocabLoury application
"""

class Icons:
    """Professional icon constants using Unicode symbols"""
    
    # Authentication
    LOGIN = "🔐"
    LOGOUT = "🚪"
    USER = "👤"
    EMAIL = "✉️"
    PASSWORD = "🔑"
    EYE = "👁️"
    EYE_SLASH = "🙈"
    
    # Navigation
    HOME = "🏠"
    PROFILE = "👤"
    DICTIONARY = "📚"
    ALPHABET = "🔤"
    SAVED = "⭐"
    LEARNING = "🎯"
    SETTINGS = "⚙️"
    
    # Actions
    SEARCH = "🔍"
    ADD = "➕"
    EDIT = "✏️"
    DELETE = "🗑️"
    SAVE = "💾"
    SHARE = "📤"
    DOWNLOAD = "⬇️"
    UPLOAD = "⬆️"
    
    # Status
    SUCCESS = "✅"
    ERROR = "❌"
    WARNING = "⚠️"
    INFO = "ℹ️"
    LOADING = "⏳"
    
    # Learning
    BOOK = "📖"
    GRADUATION = "🎓"
    TARGET = "🎯"
    TROPHY = "🏆"
    STAR = "⭐"
    HEART = "❤️"
    
    # Theme
    DARK = "🌙"
    LIGHT = "☀️"
    
    # Professional alternatives (using text symbols)
    @staticmethod
    def get_professional_icon(icon_type):
        """Get professional text-based icons"""
        professional_icons = {
            'login': '→',
            'logout': '←',
            'user': '●',
            'email': '@',
            'password': '●',
            'home': '⌂',
            'profile': '●',
            'dictionary': '📖',
            'alphabet': 'A',
            'saved': '★',
            'learning': '●',
            'search': '🔍',
            'add': '+',
            'edit': '✎',
            'delete': '×',
            'save': '💾',
            'success': '✓',
            'error': '✗',
            'warning': '!',
            'info': 'i',
            'dark': '●',
            'light': '○'
        }
        return professional_icons.get(icon_type, '●')
