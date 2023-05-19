"""
Django settings for say_wagtail project.
"""

from ._setup import *


# set env casting, default value
env = environ.Env(
    # DEBUG=(bool, False)
)


DEBUG = env.bool("DEBUG", default=False)

SECRET_KEY = env.str("SECRET_KEY")

INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS", default=["http://localhost", "http://127.0.0.1"]
)


INSTALLED_APPS = clean_ellipsis(
    [
        # fmt: off
        "say.home",
        "say.linked_account",
        "say.page_types",
        "say.search",
        "say.storage",
        "say.accounting",
        "say.core",

        "corsheaders",
        "debug_toolbar" if PLUGGABLE_FUNCS.DEBUG_TOOLBAR else ...,
        "django_browser_reload" if PLUGGABLE_FUNCS.BROWSER_RELOAD else ...,
        "django_grpc",
        "django_vite",
        "grapple",
        "graphene_django",
        "wagtail_headless_preview",

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
        # fmt: on
    ]
)

MIDDLEWARE = clean_ellipsis(
    [
        "debug_toolbar.middleware.DebugToolbarMiddleware"
        if PLUGGABLE_FUNCS.DEBUG_TOOLBAR
        else ...,
        "django.contrib.sessions.middleware.SessionMiddleware",
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        # "wagtail.contrib.redirects.middleware.RedirectMiddleware",
        "wagtail.sites.middleware.SiteUserMiddleware",
        "django_htmx.middleware.HtmxMiddleware",
        "django_browser_reload.middleware.BrowserReloadMiddleware"
        if PLUGGABLE_FUNCS.BROWSER_RELOAD
        else ...,
    ]
)

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

AUTH_USER_MODEL = "accounting.User"

AUTH_PASSWORD_VALIDATORS = (
    [
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
    if not PLUGGABLE_FUNCS.NO_PASS_VALIDATION
    else []
)


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
    os.path.join(BASE_DIR, "say", "static_dist"),
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


DEFAULT_FILE_STORAGE = "say.core.storage.DynamicLibCloudStorage"
