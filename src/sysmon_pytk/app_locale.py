# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Locale management.
"""

import os
import gettext
from configparser import ConfigParser, Error

from . import _file_utils

LANGUAGES = {
    "English": "en",
    "Español": "es"
}

__i18n_domain__ = "app"

CURRENT_LANG: str = "en"
try:
    _filename = _file_utils.settings_path()
    _config = ConfigParser()
    _config.read(_filename)
    if "general" in _config.sections():
        CURRENT_LANG = _config["general"].get("language", fallback="en")
except Error:
    pass

_localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "locale")
translation = gettext.translation(
        __i18n_domain__, _localedir, fallback=True, languages=[CURRENT_LANG]
    )
_ = translation.gettext
