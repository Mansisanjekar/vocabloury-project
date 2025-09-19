/**
 * VocabLoury - Theme Management JavaScript
 */

class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('vocabloury-theme') || 'dark';
        this.themeSelector = null;
        this.init();
    }

    init() {
        this.applyTheme(this.currentTheme);
        this.createThemeToggle();
        this.createThemeSelector();
        this.bindEvents();
    }

    createThemeToggle() {
        const toggle = document.createElement('button');
        toggle.className = 'theme-toggle';
        toggle.innerHTML = this.getThemeIcon(this.currentTheme);
        toggle.setAttribute('aria-label', 'Toggle theme');
        document.body.appendChild(toggle);
        
        toggle.addEventListener('click', () => {
            this.toggleThemeSelector();
        });
    }

    createThemeSelector() {
        const selector = document.createElement('div');
        selector.className = 'theme-selector';
        selector.innerHTML = `
            <div class="theme-options">
                <div class="theme-option" data-theme="dark" title="Dark Theme"></div>
                <div class="theme-option" data-theme="light" title="Light Theme"></div>
                <div class="theme-option" data-theme="blue" title="Blue Theme"></div>
                <div class="theme-option" data-theme="purple" title="Purple Theme"></div>
                <div class="theme-option" data-theme="green" title="Green Theme"></div>
                <div class="theme-option" data-theme="orange" title="Orange Theme"></div>
            </div>
        `;
        document.body.appendChild(selector);
        this.themeSelector = selector;
    }

    bindEvents() {
        // Theme option clicks
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('theme-option')) {
                const theme = e.target.dataset.theme;
                this.setTheme(theme);
                this.closeThemeSelector();
            }
        });

        // Close theme selector when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.theme-selector') && 
                !e.target.closest('.theme-toggle') && 
                this.themeSelector.classList.contains('open')) {
                this.closeThemeSelector();
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.themeSelector.classList.contains('open')) {
                this.closeThemeSelector();
            }
        });
    }

    setTheme(theme) {
        this.currentTheme = theme;
        localStorage.setItem('vocabloury-theme', theme);
        this.applyTheme(theme);
        this.updateActiveThemeOption();
        this.updateThemeToggleIcon();
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        
        // Update CSS custom properties
        const root = document.documentElement;
        const themes = {
            dark: {
                '--bg-primary': '#0f0f0f',
                '--bg-secondary': '#1a1a1a',
                '--bg-tertiary': '#2a2a2a',
                '--accent': '#3b82f6',
                '--accent-hover': '#2563eb',
                '--text-primary': '#ffffff',
                '--text-secondary': '#d1d5db',
                '--text-muted': '#9ca3af',
                '--border': '#374151',
                '--border-light': '#4b5563'
            },
            light: {
                '--bg-primary': '#ffffff',
                '--bg-secondary': '#f8fafc',
                '--bg-tertiary': '#f1f5f9',
                '--accent': '#3b82f6',
                '--accent-hover': '#2563eb',
                '--text-primary': '#1e293b',
                '--text-secondary': '#475569',
                '--text-muted': '#64748b',
                '--border': '#e2e8f0',
                '--border-light': '#f1f5f9'
            },
            blue: {
                '--bg-primary': '#0f172a',
                '--bg-secondary': '#1e293b',
                '--bg-tertiary': '#334155',
                '--accent': '#0ea5e9',
                '--accent-hover': '#0284c7',
                '--text-primary': '#f8fafc',
                '--text-secondary': '#cbd5e1',
                '--text-muted': '#94a3b8',
                '--border': '#475569',
                '--border-light': '#64748b'
            },
            purple: {
                '--bg-primary': '#1a0b2e',
                '--bg-secondary': '#2d1b4e',
                '--bg-tertiary': '#3d2a5e',
                '--accent': '#a855f7',
                '--accent-hover': '#9333ea',
                '--text-primary': '#f3e8ff',
                '--text-secondary': '#d8b4fe',
                '--text-muted': '#c084fc',
                '--border': '#6b46c1',
                '--border-light': '#8b5cf6'
            },
            green: {
                '--bg-primary': '#0c1b0f',
                '--bg-secondary': '#1a2e1d',
                '--bg-tertiary': '#2a3e2d',
                '--accent': '#22c55e',
                '--accent-hover': '#16a34a',
                '--text-primary': '#f0fdf4',
                '--text-secondary': '#bbf7d0',
                '--text-muted': '#86efac',
                '--border': '#4ade80',
                '--border-light': '#6ee7b7'
            },
            orange: {
                '--bg-primary': '#1c0f0a',
                '--bg-secondary': '#2d1b0f',
                '--bg-tertiary': '#3d2a1a',
                '--accent': '#f97316',
                '--accent-hover': '#ea580c',
                '--text-primary': '#fff7ed',
                '--text-secondary': '#fed7aa',
                '--text-muted': '#fdba74',
                '--border': '#fb923c',
                '--border-light': '#fdba74'
            }
        };

        const themeColors = themes[theme];
        if (themeColors) {
            Object.entries(themeColors).forEach(([property, value]) => {
                root.style.setProperty(property, value);
            });
        }
    }

    updateActiveThemeOption() {
        const options = document.querySelectorAll('.theme-option');
        options.forEach(option => {
            option.classList.remove('active');
            if (option.dataset.theme === this.currentTheme) {
                option.classList.add('active');
            }
        });
    }

    updateThemeToggleIcon() {
        const toggle = document.querySelector('.theme-toggle');
        if (toggle) {
            toggle.innerHTML = this.getThemeIcon(this.currentTheme);
        }
    }

    getThemeIcon(theme) {
        const icons = {
            dark: '🌙',
            light: '☀️',
            blue: '🔵',
            purple: '🟣',
            green: '🟢',
            orange: '🟠'
        };
        return icons[theme] || '🌙';
    }

    toggleThemeSelector() {
        if (this.themeSelector.classList.contains('open')) {
            this.closeThemeSelector();
        } else {
            this.openThemeSelector();
        }
    }

    openThemeSelector() {
        this.themeSelector.classList.add('open');
        this.updateActiveThemeOption();
    }

    closeThemeSelector() {
        this.themeSelector.classList.remove('open');
    }

    // Public method to get current theme
    getCurrentTheme() {
        return this.currentTheme;
    }

    // Public method to set theme programmatically
    switchTheme(theme) {
        this.setTheme(theme);
    }
}

// Initialize theme manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeManager;
}
