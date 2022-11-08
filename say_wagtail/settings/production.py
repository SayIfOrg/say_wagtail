from .base import *

DEBUG = False


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Manifest one is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache
# See https://docs.djangoproject.com/en/4.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = (
    "customized.storages.backends.apache_libcloud.LibCloudManifestStaticStorage"
)
DEFAULT_LIBCLOUD_STATIC_PROVIDER = "minio-static"


try:
    from .local import *
except ImportError:
    pass
