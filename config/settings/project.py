"""
Project custom settings
"""

from ._setup import *


# set env casting, default value
env = environ.Env(
    # DEBUG=(bool, False)
)


WEBFACE_URL = env.url("WEBFACE_URL")


# AVAILABLE_STORAGES = [
#     "first_minio",
# ]
