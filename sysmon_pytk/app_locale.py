# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Locale management.
"""

from __future__ import annotations

import gettext
import importlib
import inspect
from configparser import ConfigParser, Error
from pathlib import Path
from typing import TYPE_CHECKING

from .file_utils import settings_path

if TYPE_CHECKING:
    from .callables import GettextCallable

LANGUAGES = {
    "English": "en",
    "Español": "es",
    "Deutsch": "de",
    "Norsk Bokmål": "nb_NO"
}

__i18n_domain__ = "app"

TRANSLATED_MODULES: list = []


def get_translator(
    *, forced_lang: str | None = None, domain: str = __i18n_domain__
) -> GettextCallable:
    """
    Load the selected translation.
    """
    current_lang = forced_lang if forced_lang else _get_lang_from_config()
    frm = inspect.stack()[1]  # get caller
    mod = inspect.getmodule(frm.frame)
    if mod not in TRANSLATED_MODULES:
        TRANSLATED_MODULES.append(mod)
        TRANSLATED_MODULES.sort(key=lambda x: x.__name__)
    _localedir = Path.resolve(Path(__file__).parent) / "locale"
    translation = gettext.translation(
        domain, _localedir, fallback=True, languages=[current_lang]
    )
    return translation.gettext


def reload_translated_modules() -> None:
    """
    Reload any modules that have requested translations.
    """
    for mod in TRANSLATED_MODULES:
        importlib.reload(mod)


def _get_lang_from_config() -> str:
    current_lang = "en"
    try:
        _filename = settings_path()
        _config = ConfigParser()
        _config.read(_filename)
        if "general" in _config.sections():
            current_lang = _config["general"].get("language", fallback="en")
    except Error:
        pass
    return current_lang
