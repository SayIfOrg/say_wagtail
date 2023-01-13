"""
Shared code snippets for settings modules
"""

import os
import environ


# Build paths inside the project
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(CONFIG_DIR)
