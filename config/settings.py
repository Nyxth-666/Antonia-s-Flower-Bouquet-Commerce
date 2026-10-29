import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
  
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS", "localhost,127.0.0.1"
    ).split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "unfold", # For customizing Django admin, placed before "django.contrib.admin"
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "apps.core",
    "apps.accounts",
    "apps.catalog",
    "apps.occasions",
    "apps.customization",
    "apps.orders",
    "apps.about",
    "apps.contact",
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
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.navbar_data',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# UNFOLD DOCS: https://unfoldadmin.com/docs/configuration/settings/
UNFOLD = {
    "THEME": "light",
    "SITE_TITLE": "Antonia's Flowershop",
    "SITE_HEADER": "Antonia's Flowershop",
    "SITE_SUBHEADER": "Admin panel",

    "SITE_ICON": {
        "light": lambda request: static("images/logo.png"),  # light mode
        "dark": lambda request: static("images/logo.png"),  # dark mode
    },

    "LOGIN": {
        "image": lambda request: static("sample/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:APP_MODEL_changelist"),
        # Inherits from `unfold.forms.AuthenticationForm`
    },

    "STYLES": [
        lambda r: static("css/admin_output.css"),
    ],
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Management"),
                "separator": False,
                "collapsible": False,
                "items": [
                    {"title": _("Group"), "icon": "dashboard", "link": reverse_lazy("admin:auth_group_changelist")},
                    {"title": _("Users"), "icon": "people", "link": reverse_lazy("admin:auth_user_changelist")},
                ],
            },
            {
                "title": _("Catalog"),
                "separator": True,
                "collapsible": False,
                "items": [
                    {"title": _("Bouquets"), "icon": "local_florist", "link": reverse_lazy("admin:catalog_bouquet_changelist")},
                    {"title": _("Colors"), "icon": "palette", "link": reverse_lazy("admin:catalog_color_changelist")},
                    {"title": _("Flower types"), "icon": "filter_vintage", "link": reverse_lazy("admin:catalog_flowertype_changelist")},
                    {"title": _("Occasions"), "icon": "celebration", "link": reverse_lazy("admin:catalog_occasion_changelist")},
                ],
            },
        ],
    },
}