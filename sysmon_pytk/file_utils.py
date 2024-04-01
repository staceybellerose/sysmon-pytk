# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
File utility functions.
"""

import inspect
import sys
from distutils.sysconfig import get_python_lib
from pathlib import Path

import platformdirs

SETTINGS_FILE = "sysmon.ini"


def get_full_path(relative_path: str) -> str:
    """
    Get the full path of a file, based on its relative path to this project.
    """
    std_lib = Path(get_python_lib())
    if Path.is_file(std_lib / __package__):
        base_dir = (std_lib / __package__).parent
    else:
        base_dir = Path(__file__).parent
    return f"{base_dir / relative_path}"


def settings_path() -> str:
    """
    Get the full path for the settings file.
    """
    package = __package__ if __package__ else Path(__file__).parts[-2]
    base_dir = platformdirs.user_config_path(package)
    if not base_dir.exists():
        base_dir.mkdir(parents=True)
    return f"{base_dir / SETTINGS_FILE}"


def get_main_script() -> str:
    """
    Get the name of the top level running script.
    """
    for frame in reversed(inspect.stack()):
        if frame.filename.startswith(sys.exec_prefix):
            continue
        if frame.filename.startswith(sys.base_exec_prefix):
            continue
        return Path(frame.filename).name
    return ""
