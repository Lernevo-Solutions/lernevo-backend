from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

ENV = os.environ.get("ENV", "DEV")

SECRET_KEY = os.environ.get("SECRET_KEY", "local-secret-key")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]


# ================= INSTALLED APPS =================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    'rest_framework.authtoken',
    "corsheaders",
    # Replace 'api' with your actual Django app name
    "app",
]


# ================= MIDDLEWARE =================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'backend.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ================= URL / WSGI =================

ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"


# ================= TEMPLATES =================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ================= DATABASE =================

import os

ENV = os.environ.get("ENV", "DEV")
print("========== ENV value from os.environ ==========")
print("Raw ENV:", repr(ENV))  # repr() shows exact string with quotes
print("Length:", len(ENV))
print("Uppercase comparison:", ENV.strip().upper() == "PROD")
print("================================================")

if ENV.strip().upper() == "PROD":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME"),
            "USER": os.environ.get("DB_USER"),
            "PASSWORD": os.environ.get("DB_PASSWORD"),
            "HOST": f"/cloudsql/{os.environ.get('INSTANCE_CONNECTION_NAME')}",
            "PORT": "5432",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ================= PASSWORD VALIDATION =================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ================= LANGUAGE / TIME =================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"

USE_I18N = True
USE_TZ = True


# ================= STATIC =================

STATIC_URL = "/static/"


# ================= MEDIA =================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ================= CORS =================

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True


# ================= REST FRAMEWORK =================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

FRONTEND_URL = os.environ.get(
    "FRONTEND_URL",
    "https://lernevo-frontend-771297649928.us-central1.run.app"
)


# ================= EMAIL =================

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# backend/backend/settings.py
# Vertex AI Configuration
import os
import subprocess

# Get project ID – NEVER use project number
VERTEX_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
if not VERTEX_PROJECT_ID:
    try:
        VERTEX_PROJECT_ID = subprocess.check_output(
            ['gcloud', 'config', 'get-value', 'project'],
            text=True
        ).strip()
    except:
        pass

# ✅ FORCE your actual Project ID (remove the fallback number)
if not VERTEX_PROJECT_ID or VERTEX_PROJECT_ID == '771297649928':
    VERTEX_PROJECT_ID = 'lernevo-dev-1'   # <--- YOUR CORRECT PROJECT ID

VERTEX_LOCATION = os.getenv('VERTEX_LOCATION',  'us-central1')
# Use a model version that definitely exists
VERTEX_MODEL = os.getenv('VERTEX_MODEL', 'gemini-2.0-flash-exp')  # or 'gemini-1.0-pro'

print(f"✅ Vertex AI using Project: {VERTEX_PROJECT_ID}, Model: {VERTEX_MODEL}")

import psycopg2
import os

try:
    conn = psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=f"/cloudsql/{os.environ.get('INSTANCE_CONNECTION_NAME')}",
        port=5432
    )
    print("Database connection OK")
    conn.close()
except Exception as e:
    print("Database connection failed:", e)

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

