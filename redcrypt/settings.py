"""
Django settings for redcrypt project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key;
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration


load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
try:
    if os.environ.get("DEBUG") == "True":
        DEBUG = True
    else:
        DEBUG = False
except:
    DEBUG = False

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'https://*.rachitkhurana.xyz',
    'https://*.127.0.0.1',
    'https://redcrypt.rachitkhurana.repl.co',
    'https://*.redcrypt.xyz/']
INTERNAL_IPS = [
    "127.0.0.1",
]

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',  # Add this line
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.discord',
    'hunt',
    'accounts',
    'extra_settings',
    'admin_honeypot',
    'url_shortner',
    'hcaptcha',
    'maintenance_mode',
    'pwa'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'redcrypt.middleware.CustomMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]

ROOT_URLCONF = 'redcrypt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':  {
                'profile_tags': 'accounts.templatetags.profile_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'redcrypt.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# sentry_sdk.init(
#     dsn=os.getenv('SENTRY_DSN'),
#     integrations=[DjangoIntegration()],

#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production.
#     traces_sample_rate=1.0,

#     # If you wish to associate users to errors (assuming you are using
#     # django.contrib.auth) you may enable sending PII data.
#     send_default_pii=True
# )

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

SITE_ID = 3

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_FORMS = {
    'signup': 'accounts.forms.MyCustomSignupForm',
    'reset_password': 'accounts.forms.CustomForgetPassword'}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_MAX_EMAIL_ADDRESSES = 1

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True

LOGIN_REDIRECT_URL = '/profile/'
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True

APPEND_SLASH = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = True
WHITENOISE_ROOT = "static"
STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-pulse.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = "Re-Dcrypt <hunt@redcrypt.xyz>"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "Re-Dcrypt - "
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 600
SOCIALACCOUNT_AUTO_SIGNUP = False
HCAPTCHA_SITEKEY = os.getenv('HCAPTCHA_SITEKEY')
HCAPTCHA_SECRET = os.getenv('HCAPTCHA_SECRET')

try:
    if os.getenv("MAINTENANCE_MODE").lower() == "true":
        MAINTENANCE_MODE = True
    else:
        MAINTENANCE_MODE = False
except:
    MAINTENANCE_MODE = False

MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_IGNORE_SUPERUSER = True


PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'serviceworker.js')
PWA_APP_NAME = 'Re-Dcrypt'
PWA_APP_DESCRIPTION = 'Re-Dcrypt Cryptic Hunt.'
PWA_APP_THEME_COLOR = '#00d2d2'
PWA_APP_BACKGROUND_COLOR = '#002a2a'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/'
PWA_APP_HOME_PATH = '/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_DEBUG_MODE = False
PWA_APP_ICONS = [
    {
        'src': '/icons/maskable_icon_x192.png',
        'sizes': '192x192',
        'type': 'image/png',
        "purpose": "maskable"
    },
    {
        'src': '/icons/maskable_icon_x192.png',
        'sizes': '192x192',
        'type': 'image/png',
        "purpose": "any"
    },
    {
        'src': '/icons/maskable_icon_x512.png',
        'sizes': '512x512',
        'type': 'image/png',
        "purpose": "maskable"
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/icons/maskable_icon_x192.png',
        'sizes': '192x192',
        'type': 'image/png',
        "purpose": "maskable",
    },
    {
        'src': '/icons/maskable_icon_x192.png',
        'sizes': '192x192',
        'type': 'image/png',
        "purpose": "any"
    },
    {
        'src': '/icons/maskable_icon_x512.png',
        'sizes': '512x512',
        'type': 'image/png',
        "purpose": "maskable"
    }
]
PWA_APP_LANG = 'en-US'
