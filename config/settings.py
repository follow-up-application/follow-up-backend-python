from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "reports"])

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "drf_spectacular",
    "reports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "reports.idempotency.IdempotencyMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": env.db("JOBS_DATABASE_URL"),
    "follow": env.db("DATABASE_URL"),
}
DATABASES["default"]["OPTIONS"] = {"options": "-c search_path=reportes"}
DATABASE_ROUTERS = ["reports.db_router.ReportsRouter"]

SERVICE_TOKEN = env("SERVICE_TOKEN")
STORAGE_DIR = Path(env("STORAGE_DIR", default="storage/documents"))
DOCUMENT_TTL_HOURS = env.int("DOCUMENT_TTL_HOURS", default=72)
MAX_ROWS = env.int("MAX_ROWS", default=20000)

REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_TRACK_STARTED = True
CELERY_TIMEZONE = env("TIME_ZONE", default="America/Argentina/Buenos_Aires")

USE_TZ = True
TIME_ZONE = CELERY_TIMEZONE
LANGUAGE_CODE = "es-ar"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["reports.permissions.ServiceTokenPermission"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "reports.views.exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Follow Reports API",
    "DESCRIPTION": "Microservicio de generacion de reportes (PDF/XLSX) y certificados oficiales",
    "VERSION": "1.0.0",
}
