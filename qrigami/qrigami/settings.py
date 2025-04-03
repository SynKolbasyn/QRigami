"""QRigami. QR code generator site.

Copyright (C) 2025  Andrew Kozmin <syn.kolbasyn.06@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from os import environ
from pathlib import Path


def get_env_bool(key: str, *, default: bool | None = None) -> bool | None:
    """Get bool variable from env."""
    if key not in environ:
        if default:
            return default
        error_message = f"{key}"
        raise KeyError(error_message)
    return environ[key].lower() in {"y", "yes", "t", "true", "on", "1"}


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = environ.get("DJANGO_SECRET_KEY", "DJANGO_SECRET_KEY")


DEBUG = get_env_bool("DJANGO_DEBUG")


ALLOWED_HOSTS = ["*"]


if DEBUG:
    INTERNAL_IPS = ["127.0.0.1"]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "sorl.thumbnail",

    "web_authn.apps.WebAuthnConfig",

    "django_cleanup.apps.CleanupConfig",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        *MIDDLEWARE,
    ]


ROOT_URLCONF = "qrigami.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates/"],
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


WSGI_APPLICATION = "qrigami.wsgi.application"
ASGI_APPLICATION = "qrigami.asgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

if not DEBUG:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "OPTIONS": {
                "pool": True,
            },
            "HOST": environ["POSTGRES_HOST"],
            "PORT": environ["POSTGRES_PORT"],
            "USER": environ["POSTGRES_USER"],
            "PASSWORD": environ["POSTGRES_PASSWORD"],
            "NAME": environ["POSTGRES_DB"],
        },
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"
USE_TZ = True

USE_I18N = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static/"
STATICFILES_DIRS = [BASE_DIR / "static_dev/"]

MEDIA_URL = "media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


HOST = environ.get("DJANGO_HOST", "localhost")
HOST_NAME = environ.get("DJANGO_HOST_NAME", "QRigami")
ORIGIN = environ.get("DJANGO_ORIGIN", f"http://{HOST}:8000")


EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails/"

if not DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = environ["DJANGO_EMAIL_HOST"]
    EMAIL_HOST_PASSWORD = environ["DJANGO_EMAIL_HOST_PASSWORD"]
    EMAIL_HOST_USER = environ["DJANGO_EMAIL_HOST_USER"]
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    EMAIL_USE_TLS = True
    EMAIL_PORT = environ["DJANGO_EMAIL_PORT"]
