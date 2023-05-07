"""
Shared variables and code snippets for settings modules
"""

import os
from django.core.exceptions import ImproperlyConfigured
import environ


# Build paths inside the project
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(CONFIG_DIR)


# handy funcs
def clean_ellipsis(items: iter):
    return [i for i in items if i is not ...]


# set env casting, default value
env = environ.Env(
    # DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


# Define pluggable functionalities
pluggable_available = ["BROWSER_RELOAD", "NO_PASS_VALIDATION", "DEBUG_TOOLBAR"]
pluggable_enabled = env.list("PLUGGABLES")
for p in pluggable_enabled:
    if p not in pluggable_available:
        raise ImproperlyConfigured(f"{p} is not a pluggable option")


class PLUGGABLE_FUNCS:
    BROWSER_RELOAD = "BROWSER_RELOAD" in pluggable_enabled
    NO_PASS_VALIDATION = "NO_PASS_VALIDATION" in pluggable_enabled
    DEBUG_TOOLBAR = "DEBUG_TOOLBAR" in pluggable_enabled
