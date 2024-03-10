# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Locale management.
"""

import os
import gettext
from configparser import ConfigParser, Error

from _common import SETTINGS_FILE, get_full_path

LANGUAGES = {
    "English": "en",
    "Español": "es"
}

CURRENT_LANG: str = "en"
try:
    _filename = get_full_path(SETTINGS_FILE)
    _config = ConfigParser()
    _config.read(_filename)
    CURRENT_LANG = _config["general"].get("language", fallback="en")
except Error:
    pass

_localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
translation = gettext.translation(
        'app', _localedir, fallback=True, languages=[CURRENT_LANG]
    )
_ = translation.gettext
