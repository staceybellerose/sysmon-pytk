# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Tk Style Manager.
"""

import re
from typing import Any
import tkinter as tk
from tkinter import ttk, font
from tkinter.font import Font

import darkdetect

from . import font_utils
from .file_utils import get_full_path
from .settings import Settings


def is_dark(hexcolor: str) -> bool:
    """
    Determine whether a given hex color is light or dark.

    Parameters
    ----------
    hexcolor: str
        a string with the format "#xxxxxx" where x is a hex digit (0-9, A-F)

    Returns
    -------
    bool
        True when the color is determined to be dark; False otherwise.

    Examples
    --------
    >>> is_dark("#000000")
    True
    >>> is_dark("#ffffff")
    False
    >>> is_dark("#123456")
    True
    >>> is_dark("#449F55")
    False
    """
    assert len(hexcolor) == 7  # nosec B101
    assert hexcolor[:1] == "#"  # nosec B101
    if re.search(r"^#[\dA-Fa-f]{6}$", hexcolor) is None:
        raise ValueError("hexcolor must start with '#' and have 6 hexadecimal digits")
    r = int(hexcolor[1:3], 16)
    g = int(hexcolor[3:5], 16)
    b = int(hexcolor[5:7], 16)
    # calculate the square of the luminance and compare it to a cutoff value of 127.5²
    # this way, sqrt() doesn't need to be called
    hsp = 0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b)
    return hsp < 16256.25


class StyleManager:
    """
    Tk Style Manager.
    """

    @classmethod
    def get_dark_mode(cls, settings: Settings) -> bool:
        """
        Determine dark mode by checking settings or detecting the system theme.
        """
        if settings.get_theme() == "Dark":
            return True
        if settings.get_theme() == "Light":
            return False
        return darkdetect.isDark()

    @classmethod
    def init_theme(cls, root: tk.Tk, settings: Settings) -> None:
        """
        Initialize theme and styles for the application.
        """
        root.tk.call("source", get_full_path("../azure/azure.tcl"))
        cls.update_by_dark_mode(root, settings)
        cls.init_fonts(settings)
        root.option_add('*TCombobox*Listbox.font', "TkDefaultFont")

    @classmethod
    def init_fonts(cls, settings: Settings) -> None:
        """
        Initialize the fonts to be used.
        """
        base_font = font.nametofont("TkDefaultFont")
        text_font = font.nametofont("TkTextFont")
        menu_font = font.nametofont("TkMenuFont")
        fixed_font = font.nametofont("TkFixedFont")
        if settings.regular_font.get_name() != "":
            settings.regular_font.configure_font(base_font)
            settings.regular_font.configure_font(text_font)
            settings.regular_font.configure_font(menu_font)
        else:
            base_font.configure(family=font_utils.MAIN_FONT_FAMILY, size=12)
            text_font.configure(family=font_utils.MAIN_FONT_FAMILY, size=12)
            menu_font.configure(family=font_utils.MAIN_FONT_FAMILY, size=12)
        if settings.fixed_font.get_name() != "":
            settings.fixed_font.configure_font(fixed_font)
        else:
            fixed_font.configure(family=font_utils.FIXED_FONT_FAMILY, size=12)
        style = ttk.Style()
        style.configure("TButton", font="TkDefaultFont")
        style.configure("TRadiobutton", font="TkDefaultFont")
        style.configure("TLabelFrame", font="TkDefaultFont")
        style.configure("TNotebook", font="TkDefaultFont")
        style.configure("TNotebook.Tab", font="TkDefaultFont")
        style.configure("Switch.TCheckbutton", font="TkDefaultFont")
        style.configure("System.TLabel", font="TkDefaultFont")

    @classmethod
    def update_by_dark_mode(cls, root: tk.Tk, settings: Settings) -> None:
        """
        Update styles based on dark mode.
        """
        dark_mode = cls.get_dark_mode(settings)
        root.tk.call("set_theme", "dark" if dark_mode else "light")
        style = ttk.Style()
        if dark_mode:
            style.configure("Safe.TLabel", foreground="#00aa00")
            style.configure("Warn.TLabel", foreground="#ffff22")
            style.configure("Alert.TLabel", foreground="#ff2222")
            style.configure("URL.TLabel", foreground="#66ccff")
        else:
            style.configure("Safe.TLabel", foreground="#009900")
            style.configure("Warn.TLabel", foreground="#aaaa00")
            style.configure("Alert.TLabel", foreground="#cc0000")
            style.configure("URL.TLabel", foreground="#0000ee")

    @classmethod
    def test_dark_mode(cls, trueval: Any, falseval: Any) -> Any:
        """
        If currently in dark mode, return trueval; otherwise return falseval.
        """
        style = ttk.Style()
        background = style.lookup("TLabel", "background")
        if is_dark(f"{background}"):
            return trueval
        return falseval

    @classmethod
    def get_base_font(cls) -> Font:
        """
        Get the base font for use in the application.
        """
        return font.nametofont("TkDefaultFont")

    @classmethod
    def get_large_font(cls) -> Font:
        """
        Get the large font for use in the application.
        """
        return font_utils.modify_named_font(
            "TkDefaultFont", size=cls.get_base_font().actual()["size"]+4
        )

    @classmethod
    def get_bold_font(cls) -> Font:
        """
        Get the bold font for use in the application.
        """
        return font_utils.modify_named_font("TkDefaultFont", weight="bold")

    @classmethod
    def get_fixed_font(cls) -> Font:
        """
        Get the monospace font for use in the application.
        """
        return font.nametofont("TkFixedFont")
