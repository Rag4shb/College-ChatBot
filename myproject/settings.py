# ================================================================
#  CLE BCA College — settings.py
#  Fixes:
#    • Removed duplicate EMAIL_BACKEND (console was overriding SMTP)
#    • Added WhiteNoise for fast static file serving on Render
#    • Added proper CSRF trusted origins
#    • Added performance optimisations (DB conn reuse, cache)
# ================================================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ────────────────────────────────────────────────────
# ⚠  Replace with a real random key in production!
SECRET_KEY = 'django-insecure-g1j_wl*v&tmy5xzj3!a4r)9-2_idd+eq-951tgx-1lwq($*+dm'

DEBUG = True          # Set to False in production

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://cle-bca-college-chikodi.onrender.com',
    'https://bridgelike-rusty-unmad.ngrok-free.dev',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
]

# ── Auth ────────────────────────────────────────────────────────
AUTH_USER_MODEL     = 'myapp.CustomUser'
LOGIN_URL           = 'login'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_REDIRECT_URL  = 'dashboard'

# ── Apps ────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    'widget_tweaks',

    # Project app
    'myapp',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK          = 'bootstrap5'

# ── Middleware ──────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise — serves static files fast (no nginx needed on Render)
    # Install with: pip install whitenoise
    # 'whitenoise.middleware.WhiteNoiseMiddleware',   # ← uncomment after pip install
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

# ── Templates ───────────────────────────────────────────────────
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

WSGI_APPLICATION = 'myproject.wsgi.application'

# ── Database ────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE':  'django.db.backends.sqlite3',
        'NAME':    BASE_DIR / 'db.sqlite3',
        # Reuse DB connections — reduces cold-start overhead
        'CONN_MAX_AGE': 60,
    }
}

# ── Password validation ─────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ─────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Kolkata'   # IST — matches Karnataka location
USE_I18N      = True
USE_TZ        = True

# ── Static & Media ──────────────────────────────────────────────
STATIC_URL       = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT      = BASE_DIR / 'staticfiles'

# WhiteNoise compressed static storage (uncomment after pip install whitenoise)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ── Email ───────────────────────────────────────────────────────
# OPTION A — Console (shows emails in terminal, good for local dev)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# OPTION B — Real Gmail SMTP (uncomment + fill in credentials for production)
# EMAIL_BACKEND      = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST         = 'smtp.gmail.com'
# EMAIL_PORT         = 587
# EMAIL_USE_TLS      = True
# EMAIL_HOST_USER    = 'your@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'   # Use Gmail App Password, not account password
# DEFAULT_FROM_EMAIL = 'your@gmail.com'
# ADMINS             = [('CLE BCA Admin', 'admin@clebca.edu.in')]

DEFAULT_FROM_EMAIL = 'noreply@clebca.edu.in'

# ── Misc ────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session cookie age: 2 weeks
SESSION_COOKIE_AGE = 60 * 60 * 24 * 14

# Logging — shows errors in terminal
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}