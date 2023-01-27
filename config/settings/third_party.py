"""
Third Party Packages settings
"""

import shutil
from ._setup import *


# set env casting, default value
env = environ.Env(
    # DEBUG=(bool, False)
)


# Wagtail #

WAGTAIL_SITE_NAME = "say_wagtail"

WAGTAILIMAGES_IMAGE_MODEL = "utils.DSWImage"
WAGTAILIMAGES_IMAGE_FORM_BASE = "say.utils.forms.DSWImageForm"

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


# engAmirEng/wagtail settings

SITE_USER_MODEL = "user_manager.SiteUser"

PATHS_NEED_SITE = ["^/admin/"]


# django-storages #

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
            "auto_create_container": True,
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
            "auto_create_container": True,
        },
    },
}
DEFAULT_LIBCLOUD_PROVIDER = "minio-1"


# django-grpc #

GRPCSERVER = {
    "servicers": ["config.grpc.server.grpc_hook"],  # see `grpc_hook()` below
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


# django-tailwind #

TAILWIND_APP_NAME = "theme"
NPM_BIN_PATH = shutil.which("npm")
