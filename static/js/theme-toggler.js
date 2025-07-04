/**
 * 🌓 CyMate Admin Theme Toggler
 * Glassmorphism Dark/Light Theme Switcher
 */

class CyMateThemeToggler {
    constructor() {
        this.isDarkMode = this.getStoredTheme();
        this.init();
    }

    init() {
        this.createToggleButton();
        this.applyTheme(this.isDarkMode);
        this.attachEventListeners();
    }

    createToggleButton() {
        // Find the navbar-nav ul element
        const navbarNav = document.querySelector('.navbar-nav.ml-auto');
        if (!navbarNav) return;

        // Create theme toggle li element
        const themeToggleLi = document.createElement('li');
        themeToggleLi.className = 'nav-item dropdown';

        // Create the toggle button
        themeToggleLi.innerHTML = `
            <a class="nav-link theme-toggler" href="#" id="themeToggle" title="Toggle Theme">
                <i class="fas fa-moon theme-icon" id="themeIcon"></i>
            </a>
        `;

        // Insert before the user dropdown (usually last item)
        const userDropdown = navbarNav.querySelector('.nav-item.dropdown:last-child');
        if (userDropdown) {
            navbarNav.insertBefore(themeToggleLi, userDropdown);
        } else {
            navbarNav.appendChild(themeToggleLi);
        }
    }

    attachEventListeners() {
        const toggleButton = document.getElementById('themeToggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleTheme();
            });
        }
    }

    toggleTheme() {
        this.isDarkMode = !this.isDarkMode;
        this.applyTheme(this.isDarkMode);
        this.storeTheme(this.isDarkMode);
    }

    applyTheme(isDark) {
        const body = document.body;
        const html = document.documentElement;
        const themeIcon = document.getElementById('themeIcon');
        
        // Remove all existing theme classes
        body.classList.remove('cymate-dark-theme', 'cymate-light-theme');
        html.classList.remove('cymate-dark-theme', 'cymate-light-theme');
        
        // Apply the correct theme
        const themeClass = isDark ? 'cymate-dark-theme' : 'cymate-light-theme';
        body.classList.add(themeClass);
        html.classList.add(themeClass);
        
        // Update icon
        if (themeIcon) {
            themeIcon.className = isDark ? 'fas fa-sun theme-icon' : 'fas fa-moon theme-icon';
        }

        // Trigger custom event for other components
        document.dispatchEvent(new CustomEvent('themeChanged', { 
            detail: { isDark } 
        }));
    }

    getStoredTheme() {
        const stored = localStorage.getItem('cymate-admin-theme');
        // Default to light theme if no preference is stored
        return stored ? stored === 'dark' : false;
    }

    storeTheme(isDark) {
        localStorage.setItem('cymate-admin-theme', isDark ? 'dark' : 'light');
    }
}

// Apply theme immediately to prevent flash of unstyled content
(function() {
    const stored = localStorage.getItem('cymate-admin-theme');
    const isDark = stored ? stored === 'dark' : false;
    const theme = isDark ? 'cymate-dark-theme' : 'cymate-light-theme';
    document.documentElement.className += ' ' + theme;
    if (document.body) {
        document.body.classList.add(theme);
    }
})();

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CyMateThemeToggler();
});

// Handle dynamic content loading (for AJAX pages)
if (typeof jQuery !== 'undefined') {
    $(document).ajaxComplete(() => {
        if (!document.getElementById('themeToggle')) {
            new CyMateThemeToggler();
        }
    });
} 