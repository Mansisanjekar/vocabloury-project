# VocabLoury - Dictionary & Learning Application

A modern, professional dictionary and vocabulary learning application built with Python and CustomTkinter.

## Features

- **User Authentication**: Secure login/signup with password hashing
- **Dictionary Search**: Real-time word definitions using free APIs
- **Alphabet Search**: Browse words by alphabetical order
- **Word Learning**: Profession-based word recommendations
- **Saved Words**: Personal dictionary with word management
- **Professional UI**: Modern dark/light theme with animations
- **Form Validation**: Comprehensive input validation
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Web Interface**: Modern HTML/CSS/JS interface with multiple themes
- **Responsive Design**: Mobile-first, adaptive layouts
- **Theme System**: 6 professional themes (Dark, Light, Blue, Purple, Green, Orange)
- **Animations**: Smooth transitions, hover effects, and loading states
- **Interactive Elements**: Ripple effects, notifications, and dynamic content

## Project Structure

```
vocabloury-project/
├── main.py                 # Application entry point
├── booster.py             # Legacy monolithic file (to be removed)
├── authentication.db      # SQLite database
├── config/
│   └── settings.py        # Configuration and constants
├── src/
│   ├── models/
│   │   └── database.py    # Database management
│   ├── views/
│   │   ├── auth_views.py  # Authentication UI
│   │   ├── main_views.py  # Main application UI
│   │   └── notifications.py # Notification system
│   ├── controllers/
│   │   └── auth_controller.py # Authentication logic
│   ├── api/
│   │   └── dictionary_api.py  # External API integration
│   └── utils/
│       ├── validation.py  # Form validation
│       └── animations.py  # UI animations
├── static/
│   ├── images/           # Application images
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── tests/               # Unit tests
└── docs/               # Documentation
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install customtkinter pillow plyer requests
   ```
3. Run the application:

   **Desktop Application:**
   ```bash
   python main.py
   ```

   **Web Interface:**
   ```bash
   python main.py --web
   ```

   **Easy Launcher:**
   ```bash
   python launch.py
   ```

## Dependencies

- `customtkinter`: Modern UI framework
- `pillow`: Image processing
- `plyer`: Cross-platform notifications
- `requests`: HTTP API calls
- `sqlite3`: Database (built-in)

## API Integration

- **Dictionary API**: https://api.dictionaryapi.dev/
- **Datamuse API**: https://api.datamuse.com/

## Development

The application follows MVC (Model-View-Controller) architecture:

- **Models**: Database operations and data management
- **Views**: UI components and user interface
- **Controllers**: Business logic and application flow
- **Utils**: Helper functions and utilities
- **API**: External service integrations

## Features in Detail

### Authentication
- Secure password hashing with salt
- Remember me functionality
- Session management
- Form validation

### Dictionary Features
- Real-time word definitions
- Synonyms and antonyms
- Pronunciation information
- Word history tracking

### User Experience
- Professional dark/light themes
- Smooth animations
- Responsive design
- Error handling

### Styling & Themes
- **6 Professional Themes**: Dark, Light, Blue, Purple, Green, Orange
- **Modern CSS Architecture**: Component-based styling with CSS variables
- **Responsive Design**: Mobile-first approach with adaptive layouts
- **Interactive Animations**: Hover effects, transitions, and loading states
- **Theme Switching**: Smooth theme transitions with persistent preferences
- **Professional UI Components**: Cards, buttons, forms, and navigation
- **Accessibility**: High contrast, keyboard navigation, screen reader support

### Web Interface
- **Modern HTML/CSS/JS**: Professional web interface
- **Real-time Theme Switching**: Dynamic theme changes without page reload
- **Interactive Elements**: Ripple effects, notifications, and smooth animations
- **Responsive Navigation**: Adaptive sidebar and mobile-friendly layout
- **Component Library**: Reusable UI components with consistent styling

## License

This project is open source and available under the MIT License.
