"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not installed, just continue
    pass

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-oy_#gwuhu&#^k^2v^p-a_6sw0$jk%^ucz+-r0wr3+sbj@ibzv^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', '*.ngrok.io']


# Application definition

INSTALLED_APPS = [
    'jazzmin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'blog',
    'taggit',
    'corsheaders',
]

# Site ID is required for registration
SITE_ID = 1

# Rest Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# dj-rest-auth settings
REST_AUTH = {
    'USER_DETAILS_SERIALIZER': 'blog.serializer.UserSerializer',
    'TOKEN_SERIALIZER': 'dj_rest_auth.serializers.TokenSerializer',
    'PASSWORD_RESET_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'dj_rest_auth.serializers.PasswordResetConfirmSerializer',
    'PASSWORD_CHANGE_SERIALIZER': 'dj_rest_auth.serializers.PasswordChangeSerializer',
    'REGISTER_SERIALIZER': 'blog.serializer.CustomRegisterSerializer',
    'LOGIN_SERIALIZER': 'blog.serializer.CustomLoginSerializer',
}

# Authentication settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Change to 'mandatory' if you want to require email verification

# JWT settings (optional, if you want to use JWT tokens)
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
JWT_AUTH_REFRESH_COOKIE = 'my-refresh-token'

# Simple JWT settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

# Get email credentials from environment variables
CYMATE_EMAIL_USERNAME = os.getenv('CYMATE_EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Email settings for production
EMAIL_BACKEND = 'blog.email_backend.CustomSMTPEmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # SSL port
EMAIL_USE_SSL = True  # Use SSL instead of TLS
EMAIL_USE_TLS = False
EMAIL_HOST_USER = CYMATE_EMAIL_USERNAME
EMAIL_HOST_PASSWORD = EMAIL_PASSWORD
DEFAULT_FROM_EMAIL = f"CyMate <{CYMATE_EMAIL_USERNAME}>"
SERVER_EMAIL = CYMATE_EMAIL_USERNAME
EMAIL_TIMEOUT = 60

# Email verification settings
EMAIL_VERIFICATION_FROM_NAME = 'CyMate Team'
EMAIL_VERIFICATION_SUPPORT_EMAIL = 'cymate@gmail.com'


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL= '/media/'
MEDIA_ROOT= BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'blog.User'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3001",
    "http://localhost:3000",
    "http://localhost:3002",
]

# ========================================
# JAZZMIN ADMIN INTERFACE CUSTOMIZATION
# ========================================

JAZZMIN_SETTINGS = {
    # Title & Branding
    "site_title": "CyMate Admin",
    "site_header": "CyMate Admin Dashboard",
    "site_brand": "CyMate",
    "login_logo": "images/Logo.svg",  # Path to a logo for the login page
    "login_logo_dark": "images/Logo.svg",  # Path to a logo for the login page (dark theme)
    "site_logo": "images/black-Icon.svg",  # Logo for the top navbar
    "site_icon": "images/CyMate-Icon.svg",  # Favicon path
    "welcome_sign": "Welcome to CyMate Admin Dashboard",
    "copyright": "CyMate - Cybersecurity Platform",
    
    # User model
    "user_avatar": None,  # Field name on user model that contains avatar
    
    # Top navbar
    "topmenu_links": [
        # Navbar brand
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        
        # External links
        {"name": "CyMate Site", "url": "http://localhost:3000", "new_window": True},   
    ],
    
    # User menu on the right side
    "usermenu_links": [
        {"name": "CyMate Frontend", "url": "http://localhost:3000", "new_window": True},
        {"model": "auth.user"}
    ],
    
    # Side menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    
    # Menu ordering
    "order_with_respect_to": ["auth", "blog"],
    
    # Custom menu items
    "custom_links": {
        "blog": [{
            "name": "View Posts", 
            "url": "/admin/blog/post/", 
            "icon": "fas fa-blog",
            "permissions": ["blog.view_post"]
        }]
    },
    
    # 🎨 Complete Icons Set for CyMate Admin
    "icons": {
        # ========================================
        # 🔐 AUTHENTICATION & SECURITY
        # ========================================
        "auth": "fas fa-shield-alt",                    # 🛡️ Main auth app
        "auth.user": "fas fa-user-shield",              # 🔐 System users
        "auth.Group": "fas fa-users-cog",               # ⚙️ User groups
        "auth.Permission": "fas fa-key",                # 🔑 Permissions
        
        # ========================================
        # 👥 BLOG/COMMUNITY MODELS  
        # ========================================
        "blog": "fas fa-blog",                          # 📝 Main blog app
        "blog.User": "fas fa-user-circle",              # 👤 Community users
        "blog.Post": "fas fa-edit",                     # ✏️ Blog posts
        "blog.Comment": "fas fa-comments",              # 💬 Comments
        "blog.Profile": "fas fa-id-card-alt",           # 🆔 User profiles
        "blog.Notification": "fas fa-bell",             # 🔔 Notifications
        "blog.Reacts": "fas fa-heart",                  # ❤️ Reactions/likes
        "blog.Share": "fas fa-share-nodes",             # 🔗 Share functionality
        
        # ========================================
        # 🌐 SITE MANAGEMENT
        # ========================================
        "sites": "fas fa-globe-americas",               # 🌎 Sites framework
        "sites.Site": "fas fa-server",                  # 🖥️ Site configurations
        
        # ========================================
        # 📊 ADMIN & SYSTEM
        # ========================================
        "admin": "fas fa-cogs",                         # ⚙️ Admin interface
        "admin.LogEntry": "fas fa-history",             # 📜 Admin logs
        "contenttypes": "fas fa-database",              # 🗄️ Content types
        "contenttypes.ContentType": "fas fa-layer-group", # 📋 Content type objects
        "sessions": "fas fa-clock",                     # ⏰ User sessions
        "sessions.Session": "fas fa-user-clock",        # 👤⏰ Session data
        
        # ========================================
        # 🔗 API & AUTHENTICATION
        # ========================================
        "authtoken": "fas fa-lock",                     # 🔐 API tokens
        "authtoken.token": "fas fa-passport",           # 🎫 Authentication tokens (fixed!)
        "rest_framework": "fas fa-code",                # 💻 REST API
        
        # ========================================
        # 📱 SOCIAL AUTHENTICATION (AllAuth)
        # ========================================
        "account": "fas fa-user-plus",                  # ➕ Account management
        "socialaccount": "fas fa-share-alt",            # 🔗 Social accounts
        "socialaccount.SocialAccount": "fas fa-users",  # 👥 Connected social accounts
        "socialaccount.SocialApp": "fas fa-mobile-alt", # 📱 Social applications
        "socialaccount.SocialToken": "fas fa-ticket-alt", # 🎟️ Social tokens
        "account.EmailAddress": "fas fa-envelope-open", # 📧 Email addresses
        "account.EmailConfirmation": "fas fa-envelope-circle-check", # ✅ Email confirmations
        
        # ========================================
        # 🏷️ TAGGING SYSTEM
        # ========================================
        "taggit": "fas fa-tags",                        # 🏷️ Tag system
        "taggit.Tag": "fas fa-tag",                     # 🏷️ Individual tags
        "taggit.TaggedItem": "fas fa-bookmark",         # 🔖 Tagged content
        
        # ========================================
        # 🌐 CORS & HEADERS
        # ========================================
        "corsheaders": "fas fa-globe-europe",           # 🌍 CORS configuration
        
        # ========================================
        # 🔄 REST AUTH & REGISTRATION
        # ========================================
        "dj_rest_auth": "fas fa-user-lock",             # 🔐 REST authentication
        "registration": "fas fa-user-edit",             # ✏️ User registration
        
        # ========================================
        # 💻 MESSAGES & STATICFILES
        # ========================================
        "messages": "fas fa-envelope",                  # 📨 Django messages
        "staticfiles": "fas fa-folder-open",            # 📁 Static files
        
        # ========================================
        # 🔧 CUSTOM APP ICONS (if you add more apps)
        # ========================================
        # Add your future apps here with appropriate icons
        # "your_app": "fas fa-icon-name",
    },
    
    # Default model icons
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related modal
    "related_modal_active": False,
    
    # Custom CSS/JS for advanced color customization
    "custom_css": "css/cymate-admin.css",  # Custom CSS file for glassmorphism theme
    "custom_js": "js/theme-toggler.js",  # Custom JS file for theme toggling
    
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    
    # Changelist format
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible", 
        "auth.group": "vertical_tabs"
    },
    
    # Language chooser
    "language_chooser": False,
}

# UI Tweaks for Jazzmin - Glassmorphism Purple Theme
JAZZMIN_UI_TWEAKS = {
    # ============================================
    # 🎨 GLASSMORPHISM PURPLE CYBERSECURITY THEME
    # ============================================
    
    # Text sizes - Clean and modern
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    
    # Theme colors (work with our custom CSS)
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    "navbar": "navbar-dark navbar-primary",
    
    # Sidebar configuration for glassmorphism
    "sidebar_disable_expand": False,
    "sidebar_nav_small_text": False,
    "sidebar_nav_flat_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_compact_style": True,
    "sidebar": "sidebar-dark-primary",
    
    # Modern dark theme base
    "theme": "lux",  # Light base theme that works well with our custom CSS
       
    # Enhanced UI features
    "actions_sticky_top": True,
    
    # Button styling (all purple with custom CSS)
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-primary",
        "info": "btn-primary", 
        "warning": "btn-primary",
        "danger": "btn-primary",
        "success": "btn-primary"
    }
}

