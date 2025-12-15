# config/settings.py
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ============ DECOUPLE O'RNIGA ODDIY QIYMATLAR ============

SECRET_KEY = 'django-insecure-_xu(&!2&syq3*$40xcdw+2p1+u+srca*6%p0t7ukr5_$e0=s@s'
DEBUG = True
ALLOWED_HOSTS = ['*']

# ============ QOLGAN SOZLAMALAR ============

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_recaptcha',  # Faqat bu qator
    'configapp',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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
                'configapp.context_processors.profile_processor',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============ RECAPTCHA CONFIGURATION ============
RECAPTCHA_PUBLIC_KEY = "6LdtLRwsAAAAABp2xbzkwnH0sqjmby5833Md8G4D"
RECAPTCHA_PRIVATE_KEY = "6LdtLRwsAAAAANgA4Vm0Nz2ZafdEMRojP4D6j1bV"
RECAPTCHA_SITE_KEY = RECAPTCHA_PUBLIC_KEY
RECAPTCHA_SECRET_KEY = RECAPTCHA_PRIVATE_KEY
RECAPTCHA_REQUIRED_SCORE = 0.85

# ============ EMAIL CONFIGURATION ============
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jurayevmarat23@gmail.com'
EMAIL_HOST_PASSWORD = 'azvh sizw prhb ajbm'
DEFAULT_FROM_EMAIL = 'jurayevmarat23@gmail.com'
ADMIN_EMAIL = 'jurayevmarat23@gmail.com'

# ============ LOGIN/LOGOUT REDIRECTS ============
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/admin-panel/'
LOGOUT_REDIRECT_URL = '/'

# ============ FILE UPLOAD SETTINGS ============
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# ============ SESSION SETTINGS ============
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_SAVE_EVERY_REQUEST = True

# ============ MESSAGE STORAGE ============
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# ============ CUSTOM SETTINGS ============
PORTFOLIO_ITEMS_PER_PAGE = 9