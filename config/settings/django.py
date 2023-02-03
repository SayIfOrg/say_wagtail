"""
Django settings for say_wagtail project.
"""

from ._setup import *


# set env casting, default value
env = environ.Env(
    # DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


DEBUG = env.bool("DEBUG", default=False)

SECRET_KEY = env.str("SECRET_KEY")

INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=["http://localhost", "http://127.0.0.1"]
)


INSTALLED_APPS = [
    "say.home",
    "say.linked_account",
    "say.search",
    "say.storage",
    "say.super_page",
    "say.theme",
    "say.user_manager",
    "say.utils",

    "corsheaders",
    "django_browser_reload",
    "django_grpc",
    "tailwind",

    "wagtail",
    "wagtail.admin",
    "wagtail.api.v2",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.modeladmin",
    "wagtail.documents",
    "wagtail.embeds",
    "wagtail.images",
    "wagtail.search",
    "wagtail.sites",
    "wagtail.snippets",
    "wagtail.users",

    "modelcluster",
    "rest_framework",
    "taggit",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "wagtail.sites.middleware.SiteUserMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "say", "templates"),
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

WSGI_APPLICATION = "config.wsgi.application"


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


DATABASES = {
    # default
    "default": env.db_url("DATABASE_URL")
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CACHES = {
    # default
    "default": env.cache_url("CACHE_URL")
}


AUTHENTICATION_BACKENDS = [
    "wagtail.sites.backends.SiteAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "user_manager.User"

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
AUTH_PASSWORD_VALIDATORS = []


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "say", "static"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = "/media/"


# STATICFILES_STORAGE = (
#     "say.customized.storages.backends.apache_libcloud.LibCloudManifestStaticStorage"
# )
# DEFAULT_LIBCLOUD_STATIC_PROVIDER = "minio-static"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


DEFAULT_FILE_STORAGE = "say.utils.storage.DynamicLibCloudStorage"
