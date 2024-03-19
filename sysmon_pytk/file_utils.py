# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
File utility functions.
"""

import os
from distutils.sysconfig import get_python_lib
from pathlib import Path

SETTINGS_FILE = "sysmon.ini"


def get_full_path(relative_path: str) -> str:
    """
    Get the full path of a file, based on its relative path to this project.
    """
    if os.path.isfile(Path.joinpath(Path(get_python_lib()), __package__)):
        base_dir = Path.joinpath(Path(get_python_lib()), __package__).parent
    else:
        base_dir = Path(__file__).parent
    return f"{base_dir.joinpath(relative_path)}"


def settings_path() -> str:
    """
    Get the full path for the settings file.
    """
    package = __package__ if __package__ != "" else Path(__file__).parts[-2]
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home is not None:
        base_dir = Path(xdg_config_home).joinpath(package)
    else:
        base_dir = Path.home().joinpath(package)
    if not base_dir.exists():
        base_dir.mkdir()
    return f"{base_dir.joinpath(SETTINGS_FILE)}"
