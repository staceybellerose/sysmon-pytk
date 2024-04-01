# SPDX-FileCopyrightText: © 2017-2024 Akuli
# SPDX-FileCopyrightText: © 2024 Stacey Adams
# SPDX-License-Identifier: MIT

"""
Installs an entry in the desktop menu system.

You can enable it in Settings.
This plugin doesn't do anything on Windows or MacOS.

Originally from https://github.com/Akuli/porcupine/blob/main/porcupine/plugins/desktop_menu.py
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess  # nosec B404
from pathlib import Path
from typing import TYPE_CHECKING

import platformdirs

from .app_locale import get_translator
from .file_utils import get_full_path
from .modals import messagebox

if TYPE_CHECKING:
    from tkinter import Tk, Toplevel

_ = get_translator()

setup_after = ["filetypes"]  # To group the checkbutton on the bottom

XDG_DESKTOP_MENU = "xdg-desktop-menu"
DESKTOP_FILE_NAME = "sysmon.desktop"
EXECUTABLE = "sysmon"


def install_desktop_file(parent: Tk | Toplevel) -> bool:
    """
    Install a desktop menu file.
    """
    location = shutil.which(EXECUTABLE)
    if location is None:
        messagebox.show_error(
            parent, _("Error creating desktop menu item"),
            _("System Monitor (sysmon) must be installed in a virtual "
                "environment in order to create a desktop menu entry.")
        )
        return False

    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        activate_path = Path(venv) / "bin" / "activate"
        if not activate_path.is_file():
            raise FileExistsError(activate_path)
        # Must activate the venv, otherwise various things don't work
        # (e.g. os.environ.get("VIRTUAL_ENV") in this plugin)
        # %F is a list of filenames that are already quoted, so we cannot place that inside quotes.
        # Instead we need https://unix.stackexchange.com/a/144519
        bash_command = f'source {shlex.quote(str(activate_path))} && {EXECUTABLE} "$@"'
        exec_line = f"Exec=bash -c {shlex.quote(bash_command)} bash %F\n"
    else:
        exec_line = f"Exec={location}"

    launcher_path = platformdirs.user_config_path("sysmon_pytk") / DESKTOP_FILE_NAME

    with launcher_path.open("w") as file:
        file.write("[Desktop Entry]\n")
        file.write("Name=" + _("System Monitor") + "\n")
        file.write("GenericName=System Monitor\n")
        file.write(f"{exec_line}\n")
        file.write("Terminal=false\n")
        file.write("Type=Application\n")
        file.write("Categories=Monitor;System;\n")
        file.write(f"Icon={(Path(get_full_path('.')) / 'images' / 'icon-lg.png').absolute()}\n")

    subprocess.call(
        [XDG_DESKTOP_MENU, "install", "--mode", "user", "--novendor", launcher_path]
    )  # nosec B603
    launcher_path.unlink()
    return True


def uninstall_desktop_file() -> None:
    """
    Uninstall the desktop menu file.
    """
    subprocess.call(
        [XDG_DESKTOP_MENU, "uninstall", "--mode", "user", DESKTOP_FILE_NAME]
    )  # nosec B603
