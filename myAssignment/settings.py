from pathlib import Path
# import dj_database_url
import os
# from decouple import config

# Ensure BASE_DIR is correctly defined
BASE_DIR = Path(__file__).resolve().parent.parent  

SECRET_KEY = 'django-insecure-d=zn_)xtuaxrj)@5rvaoui*78$o5!xnpmf=^(%27lid#-6&vb!'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',"enfund-assignment-production.up.railway.app"]

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SITE_URL = "https://enfund-assignment-production.up.railway.app"
# ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"



INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "user",
    "channels",
    "rest_framework",
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'myAssignment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'myAssignment.wsgi.application'
ASGI_APPLICATION = "myAssignment.asgi.application"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Ensure ENGINE is correctly set
        'NAME': BASE_DIR / "db.sqlite3",  # SQLite database file
    }
}


# DATABASES = {
#     "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
# }

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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Apply WhiteNoise settings
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
]

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
)

SITE_ID = 1

LOGIN_REDIRECT_URL = "https://enfund-assignment-production.up.railway.app/upload_to_drive/"
# LOGIN_REDIRECT_URL = "http://127.0.0.1:2025/accounts/google/login/callback/"
LOGOUT_REDIRECT_URL = "https://enfund-assignment-production.up.railway.app/"

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
SOCIALACCOUNT_STORE_TOKENS = True

SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "myAssignment/config", "google_credentials.json")


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'email',
            'profile',
            'openid',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online'
        },
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
            'key': GOOGLE_CLIENT_ID,  # Add the `key` as the client_id
        },
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

CSRF_TRUSTED_ORIGINS = [
    "https://enfund-assignment-production.up.railway.app",  # Add your domain
]
