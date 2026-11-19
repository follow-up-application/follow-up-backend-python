from pathlib import Path
import environ

# Directorio raiz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga de variables de entorno desde el archivo .env
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

# Seguridad basica
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1", "reports"])

# Aplicaciones instaladas (minimas y especializadas para la API de reportes)
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
    "drf_spectacular",
    "reports",
]

# Middlewares basicos
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Configuracion de Doble Base de Datos
DATABASES = {
    "default": env.db("JOBS_DATABASE_URL"),
    "follow": env.db("DATABASE_URL"),
}
# Forzar a que la conexion 'default' busque y guarde en el esquema 'reportes'
DATABASES["default"]["OPTIONS"] = {"options": "-c search_path=reportes"}

# Router de base de datos que separa lectura academica de tablas de control
DATABASE_ROUTERS = ["reports.db_router.ReportsRouter"]

# Configuracion del microservicio
SERVICE_TOKEN = env("SERVICE_TOKEN")
STORAGE_DIR = Path(env("STORAGE_DIR", default="storage/documents"))
DOCUMENT_TTL_HOURS = env.int("DOCUMENT_TTL_HOURS", default=72)
MAX_ROWS = env.int("MAX_ROWS", default=20000)

# Cola de tareas Celery (Redis)
REDIS_URL = env("REDIS_URL", default="redis://localhost:6379/0")
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_TASK_TRACK_STARTED = True
CELERY_TIMEZONE = env("TIME_ZONE", default="America/Argentina/Buenos_Aires")

# Internacionalizacion
USE_TZ = True
TIME_ZONE = CELERY_TIMEZONE
LANGUAGE_CODE = "es-ar"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework y OpenAPI (Swagger)
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Follow Reports API",
    "DESCRIPTION": "Microservicio de generacion de reportes (PDF/XLSX) y certificados oficiales",
    "VERSION": "1.0.0",
}
