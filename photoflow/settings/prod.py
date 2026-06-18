from .base import *


DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "photoflow-8wed.onrender.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "HOST": os.environ["POSTGRES_HOST"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "PORT": int(os.environ["POSTGRES_DB_PORT"]),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
