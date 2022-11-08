from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-ds%)=v@@@9p4z8(f5&b33k0%y@n!g8*x=9o=jaf)7s@$(kx6)q"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


AUTH_PASSWORD_VALIDATORS = []


STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")


try:
    from .local import *
except ImportError:
    pass
