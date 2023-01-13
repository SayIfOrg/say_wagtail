from .base import *
import shutil

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ds%)=v@@@9p4z8(f5&b33k0%y@n!g8*x=9o=jaf)7s@$(kx6)q"

INTERNAL_IPS = [
    "127.0.0.1",
]

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


INSTALLED_APPS.extend(["django_browser_reload"])

MIDDLEWARE.extend(["django_browser_reload.middleware.BrowserReloadMiddleware"])


AUTH_PASSWORD_VALIDATORS = []


STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")


# django-tailwind configs

TAILWIND_APP_NAME = "theme"
NPM_BIN_PATH = shutil.which("npm")


try:
    from .local import *
except ImportError:
    pass
