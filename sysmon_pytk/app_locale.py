# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Locale management.
"""

import os
import gettext
import inspect
import importlib
from configparser import ConfigParser, Error

from .file_utils import settings_path

LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Deutsch": "de",
    "Norsk Bokmål": "nb_NO"
}

__i18n_domain__ = "app"

TRANSLATED_MODULES: list = []


def get_translator():
    """
    Load the selected translation.
    """
    current_lang = "en"
    try:
        _filename = settings_path()
        _config = ConfigParser()
        _config.read(_filename)
        if "general" in _config.sections():
            current_lang = _config["general"].get("language", fallback="en")
    except Error:
        pass
    frm = inspect.stack()[1]  # get caller
    mod = inspect.getmodule(frm.frame)
    if mod not in TRANSLATED_MODULES:
        TRANSLATED_MODULES.append(mod)
        TRANSLATED_MODULES.sort(key=lambda x: x.__name__)
    _localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "locale")
    translation = gettext.translation(
            __i18n_domain__, _localedir, fallback=True, languages=[current_lang]
        )
    return translation.gettext


def reload_translated_modules():
    """
    Reload any modules that have requested translations.
    """
    for mod in TRANSLATED_MODULES:
        importlib.reload(mod)
