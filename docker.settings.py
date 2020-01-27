import warnings
import copy
import os
import json

from django.utils import timezone

from .settings_common import *  # noqa


HOSTNAME = os.environ.get("HOSTNAME", "")
TEMBA_HOST = os.environ.get("TEMBA_HOST", HOSTNAME)
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", HOSTNAME).split(";")
IP_ADDRESSES = tuple(filter(None, os.environ.get("IP_ADDRESSES", "").split(",")))

SECRET_KEY = os.environ.get("SECRET_KEY", "secret-here")

DEBUG = os.environ.get("DEBUG", "false") == "true"
DEBUG_TOOLBAR = os.environ.get("DEBUG_TOOLBAR", "false") == "true"
IS_PROD = os.environ.get("IS_PROD", "false") == "true"

INSTALLED_APPS = (
    INSTALLED_APPS +
    tuple(filter(None, os.environ.get("EXTRA_INSTALLED_APPS", "").split(","))) +
    ("storages", "raven.contrib.django.raven_compat")
)

EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "false") == "true"

SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", "true") == "true"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "true") == "true"

FLOW_FROM_EMAIL = DEFAULT_FROM_EMAIL

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_PW = os.environ.get("REDIS_PW", None)
REDIS_DB = int(os.environ.get("REDIS_DB", 10))

if REDIS_PW:
    REDIS_LOCATION = "redis://:%s@%s:%s/%s" % (REDIS_PW, REDIS_HOST, REDIS_PORT, REDIS_DB)
else:
    REDIS_LOCATION = "redis://%s:%s/%s" % (REDIS_HOST, REDIS_PORT, REDIS_DB)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        }
    }
}

BROKER_URL = CACHES["default"]["LOCATION"]

_default_database_config = {
    "ENGINE": "django.contrib.gis.db.backends.postgis",
    "NAME": os.environ.get("DB_NAME", ""),
    "USER": os.environ.get("DB_USER", ""),
    "PASSWORD": os.environ.get("DB_PASSWORD", ""),
    "HOST": os.environ.get("DB_HOST", ""),
    "PORT": int(os.environ.get("DB_PORT", "5432")),
    "ATOMIC_REQUESTS": os.environ.get("DB_ATOMIC_REQUESTS", "true") == "true",
    "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", 60)),
    "OPTIONS": json.loads(os.environ.get("DB_OPTIONS", "{}"))
}

_direct_database_config = _default_database_config.copy()
_default_database_config["DISABLE_SERVER_SIDE_CURSORS"] = True

DATABASES = {"default": _default_database_config, "direct": _direct_database_config}

INTERNAL_IPS = ("*",)

MIDDLEWARE = ("temba.middleware.ExceptionMiddleware",) + MIDDLEWARE

CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_BACKEND = "redis"

warnings.filterwarnings(
    "error", r"DateTimeField .* received a naive datetime", RuntimeWarning, r"django\.db\.models\.fields"
)

# -----------------------------------------------------------------------------------
# Make our sitestatic URL be our static URL on development
# -----------------------------------------------------------------------------------
STATIC_URL = "/sitestatic/"

SEND_MESSAGES = os.environ.get("SEND_MESSAGES", "true") == "true"
SEND_WEBHOOKS = os.environ.get("SEND_WEBHOOKS", "true") == "true"
SEND_EMAILS = os.environ.get("SEND_EMAILS", "true") == "true"
SEND_AIRTIME = os.environ.get("SEND_AIRTIME", "true") == "true"
SEND_CHATBASE = os.environ.get("SEND_CHATBASE", "true") == "true"
SEND_CALLS = os.environ.get("SEND_CALLS", "true") == "true"

BRANDING["rapidpro.io"]["name"] = os.environ.get("BRANDING_NAME", "RapidPro")
BRANDING["rapidpro.io"]["description"] = os.environ.get("BRANDING_DESCRIPTION", "Visually build nationally scalable mobile applications from anywhere in the world.")
BRANDING["rapidpro.io"]["slug"] = os.environ.get("BRANDING_SLUG", "rapidpro")
BRANDING["rapidpro.io"]["credits"] = os.environ.get("BRANDING_CREDITS",
                                                    f"Copyright &copy; {timezone.now().year}. All Rights Reserved.")
BRANDING["rapidpro.io"]["link"] = os.environ.get("BRANDING_LINK", f"https://{HOSTNAME}")
BRANDING["rapidpro.io"]["api_link"] = os.environ.get("BRANDING_API_LINK", f"https://{HOSTNAME}")
BRANDING["rapidpro.io"]["domain"] = f"{HOSTNAME}"
BRANDING["rapidpro.io"]["email"] = os.environ.get("BRANDING_EMAIL", "")
BRANDING["rapidpro.io"]["support_email"] = os.environ.get("BRANDING_EMAIL_SUPPORT", "")
BRANDING["rapidpro.io"]["colors"] = dict(primary=os.environ.get("BRANDING_PRIMARY_COLOR", "#569D9B"))
BRANDING["rapidpro.io"]["favico"] = os.environ.get("BRANDING_FAVICO", "brands/rapidpro/icon.png")
BRANDING["rapidpro.io"]["allow_signups"] = os.environ.get("BRANDING_ALLOW_SIGNUPS", "true") == "true"
BRANDING["rapidpro.io"]["welcome_packs"] = [dict(size=500, name="Trial"),
                                            dict(size=2500, name="Bronze"),
                                            dict(size=30000, name="Silver"),
                                            dict(size=100000, name="Gold")]
BRANDING["rapidpro.io"]["welcome_topup"] = int(os.environ.get("BRANDING_WELCOME_TOPUP", "1000"))

COMPRESS_ENABLED = os.environ.get("COMPRESS_ENABLED", "true") == "true"
COMPRESS_OFFLINE = False

LOGGING["root"]["level"] = os.environ.get("DJANGO_LOG_LEVEL", "INFO")

RAVEN_CONFIG = {
    "dsn": os.environ.get("RAVEN_DSN")
}

AWS_S3_ENABLED = os.environ.get("AWS_S3_ENABLED", "true") == "true"

if AWS_S3_ENABLED:
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "")
    AWS_QUERYSTRING_AUTH = os.environ.get("AWS_QUERYSTRING_AUTH", "false") == "true"
    AWS_DEFAULT_ACL = os.environ.get("AWS_DEFAULT_ACL", "")
    AWS_S3_FILE_OVERWRITE = os.environ.get("AWS_S3_FILE_OVERWRITE", "false") == "true"
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "")

    # bucket where archives files are stored
    ARCHIVE_BUCKET = os.environ.get("ARCHIVE_BUCKET", "")

    AWS_BUCKET_DOMAIN = os.environ.get("AWS_BUCKET_DOMAIN", "")
    MEDIA_URL = f"https://{AWS_BUCKET_DOMAIN}/media/"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
else:
    AWS_BUCKET_DOMAIN = f"{HOSTNAME}/media"

STORAGE_URL = os.environ.get("STORAGE_URL", "/media")

REST_HANDLE_EXCEPTIONS = os.environ.get("REST_HANDLE_EXCEPTIONS", "true") == "true"

MAILROOM_URL = os.environ.get("MAILROOM_URL", "http://localhost:8090")
MAILROOM_AUTH_TOKEN = os.environ.get("MAILROOM_AUTH_TOKEN", "")

ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")

MSG_FIELD_SIZE = int(os.environ.get("MSG_FIELD_SIZE", 640))
VALUE_FIELD_SIZE = int(os.environ.get("VALUE_FIELD_SIZE", 640))
FLOWRUN_FIELDS_SIZE = int(os.environ.get("FLOWRUN_FIELDS_SIZE", 256))
