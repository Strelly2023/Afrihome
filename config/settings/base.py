# config/settings/base.py

import os
from pathlib import Path

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]   # /config/settings/base.py → up 2 levels to project root

# ------------------------------------------------------------------
# Environment
# ------------------------------------------------------------------
def env_str(name: str, default: str | None = None) -> str:
    val = os.getenv(name, default)
    if val is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

def env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.lower() in ("1", "true", "yes", "on")

def env_int(name: str, default: int | None = None) -> int:
    v = os.getenv(name)
    if v is None:
        if default is None:
            raise RuntimeError(f"Missing required env var: {name}")
        return default
    return int(v)

# ------------------------------------------------------------------
# Core Django
# ------------------------------------------------------------------
SECRET_KEY = env_str("DJANGO_SECRET_KEY", "dev-only-override-in-prod")
DEBUG = env_bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# Application definition
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # === AfriHome Platform (Phase 0 governance-first; no product domains here)
    # Wire platform orchestrators; their infra adapters live elsewhere.
    # You can add your app configs, e.g.:
    # "control_plane.tenancy.apps.TenancyConfig",
    # "control_plane.identity.apps.IdentityConfig",
    # "control_plane.access_control.apps.AccessControlConfig",
    # "control_plane.policy.apps.PolicyConfig",
    # "control_plane.organization.apps.OrganizationConfig",
    # "control_plane.events.apps.PlatformEventsConfig",
    # "control_plane.audit.apps.PlatformAuditConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    # === AfriHome: bind ExecutionContext per request (tenant + actor)
    # implemented in platform/api/middleware.py (see below)
    # "control_plane.api.middleware.ExecutionContextMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR / "templates")],
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

WSGI_APPLICATION = "config.wsgi.application"

# ------------------------------------------------------------------
# Database (keep DB adapter out of core; values from env)
# ------------------------------------------------------------------
# For dev: sqlite by default. Prod overrides to Postgres via env.
DATABASE_ENGINE = os.getenv("DB_ENGINE", "django.db.backends.sqlite3")
if DATABASE_ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": DATABASE_ENGINE,
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DATABASE_ENGINE,  # e.g. "django.db.backends.postgresql"
            "NAME": env_str("DB_NAME"),
            "USER": env_str("DB_USER"),
            "PASSWORD": env_str("DB_PASSWORD"),
            "HOST": env_str("DB_HOST", "127.0.0.1"),
            "PORT": env_str("DB_PORT", "5432"),
            "CONN_MAX_AGE": env_int("DB_CONN_MAX_AGE", 60),
            "OPTIONS": {},
        }
    }

# ------------------------------------------------------------------
# Password validation
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ------------------------------------------------------------------
# I18N / TZ (deterministic)
# ------------------------------------------------------------------
LANGUAGE_CODE = os.getenv("DJANGO_LANG", "en-us")
TIME_ZONE = os.getenv("DJANGO_TZ", "UTC")
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static/Media (infra adapters wire storage later)
# ------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR / ".static")   # Collectstatic for prod
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / ".media")

# ------------------------------------------------------------------
# Security headers (baseline; prod strengthens further)
# ------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", not DEBUG)
CSRF_COOKIE_SECURE = env_bool("CSRF_COOKIE_SECURE", not DEBUG)
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if os.getenv("CSRF_TRUSTED_ORIGINS") else []
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# ------------------------------------------------------------------
# HSTS in prod (override in prod.py)
# ------------------------------------------------------------------
SECURE_HSTS_SECONDS = env_int("SECURE_HSTS_SECONDS", 0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool("SECURE_HSTS_INCLUDE_SUBDOMAINS", False)
SECURE_HSTS_PRELOAD = env_bool("SECURE_HSTS_PRELOAD", False)

# ------------------------------------------------------------------
# Logging (structured, deterministic)
# ------------------------------------------------------------------
LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": (
                '{"level":"%(levelname)s","ts":"%(asctime)s","logger":"%(name)s",'
                '"msg":"%(message)s","module":"%(module)s","func":"%(funcName)s","line":%(lineno)d}'
            ),
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
        "console": {"format": "%(levelname)s %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "json": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"handlers": ["json"], "level": LOG_LEVEL},
}

# ------------------------------------------------------------------
# AfriHome Platform Integration Points
# (no imports here from infra; wire via platform/bootstrap at runtime)
# ------------------------------------------------------------------

# Example: toggle to enable event publishing to outbox
PLATFORM_EVENTS_ENABLED = env_bool("PLATFORM_EVENTS_ENABLED", True)

# Example: execution middleware options
EXECUTION_CONTEXT_HEADER_TENANT = os.getenv("EXEC_CTX_TENANT_HEADER", "X-AfriHome-Tenant")
EXECUTION_CONTEXT_HEADER_ACTOR  = os.getenv("EXEC_CTX_ACTOR_HEADER", "X-AfriHome-Actor")