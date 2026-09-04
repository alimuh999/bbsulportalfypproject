"""
Django settings for config project.
"""

from pathlib import Path
import os

from dotenv import load_dotenv
import dj_database_url


# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================================================
# ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv(BASE_DIR / ".env")


# ==========================================================
# OPENROUTER API
# ==========================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")


# ==========================================================
# SECURITY
# ==========================================================

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-change-this-secret-key"
)

DEBUG = os.getenv("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]


# ==========================================================
# APPLICATIONS
# ==========================================================

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Project apps
    "accounts",
    "academics",
    "finance",
    "requests_app",
    "transport",
    "examinations",
    "leaves",
    "gatepasses",
    "degree_clearance",
    "assistant",
]


# ==========================================================
# MIDDLEWARE
# ==========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==========================================================
# URL CONFIGURATION
# ==========================================================

ROOT_URLCONF = "config.urls"


# ==========================================================
# TEMPLATES
# ==========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==========================================================
# WSGI
# ==========================================================

WSGI_APPLICATION = "config.wsgi.application"


# ==========================================================
# DATABASE
# ==========================================================

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=0,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ==========================================================
# INTERNATIONALIZATION
# ==========================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Karachi"

USE_I18N = True

USE_TZ = True


# ==========================================================
# STATIC FILES
# ==========================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"


# ==========================================================
# MEDIA FILES
# ==========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ==========================================================
# EMAIL
# ==========================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ==========================================================
# DEFAULT PRIMARY KEY
# ==========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"