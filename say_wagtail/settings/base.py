"""
Django settings for say_wagtail project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "django_grpc",
    "tailwind",
    "theme",

    "linked_account",
    "super_page",
    "user_manager",
    "utils",

    "home",
    "search",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.contrib.settings",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "user_manager.middleware.ProjectUserMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "say_wagtail.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
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

WSGI_APPLICATION = "say_wagtail.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "say_wagtail",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "blog-db",
        "PORT": "5432",
    }
}

# The cache backends to use.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "cache"),
    }
}


# Apache libcloud storage provided by django-storages
LIBCLOUD_PROVIDERS = {
    "minio-static": {
        "type": "libcloud.storage.types.Provider.MINIO",
        "user": "RUf0ZRYlZy7T5qNM",
        "key": "g9g6BNic7R9xZJBlPGgbqTSwpOmYYOBm",
        "bucket": "static",
        "extra": {
            "host": "127.0.0.1",
            "port": 9000,
            "secure": False,
            "auto_create_container": True
        },
    },
    "minio-1": {
        "type": "libcloud.storage.types.Provider.MINIO",
        "user": "RUf0ZRYlZy7T5qNM",
        "key": "g9g6BNic7R9xZJBlPGgbqTSwpOmYYOBm",
        "bucket": "test",
        "extra": {
            "host": "127.0.0.1",
            "port": 9000,
            "secure": False,
            "auto_create_container": True
        },
    }
}


PATHS_NEED_SITE = ["^/admin/"]

AUTH_USER_MODEL = "user_manager.User"


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_URL = "/static/"


DEFAULT_FILE_STORAGE = 'utils.storage.DynamicLibCloudStorage'
DEFAULT_LIBCLOUD_PROVIDER = "minio-1"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail settings

WAGTAIL_SITE_NAME = "say_wagtail"

WAGTAILIMAGES_IMAGE_MODEL = "utils.DSWImage"
# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"


# django-grpc configs
GRPCSERVER = {
    "servicers": ["say_wagtail.grpc.server.grpc_hook"],  # see `grpc_hook()` below
    "interceptors": [
        # 'dotted.path.to.interceptor_class',
    ],  # optional, interceprots are similar to middleware in Django
    "maximum_concurrent_rpcs": None,
    "options": [
        ("grpc.max_receive_message_length", 1024 * 1024 * 100)
    ],  # optional, list of key-value pairs to configure the channel. The full list of available channel arguments: https://grpc.github.io/grpc/core/group__grpc__arg__keys.html
    # 'credentials': [
    #     {
    #     'private_key': 'private_key.pem',
    #     'certificate_chain': 'certificate_chain.pem'
    #     }
    # ],    # required only if SSL/TLS support is required to be enabled
    "async": False,  # Default: False, if True then gRPC server will start in ASYNC mode
}
