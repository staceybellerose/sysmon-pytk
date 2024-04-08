# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Various Tk widgets.
"""

from . import buttons, meters
from .autoscrollbar import AutoScrollbar
from .dropdown import DropDown
from .edit_menu import EditMenu, EditMenuImages
from .meter import Meter
from .scalespinner import ScaleSpinner
from .scrolling_text import ScrollingText
from .tooltip import TempToolTip, TextToolTip, ToolTip
from .url_label import UrlLabel

__all__ = [
    "AutoScrollbar",
    "DropDown",
    "EditMenuImages",
    "EditMenu",
    "Meter",
    "ScaleSpinner",
    "ScrollingText",
    "ToolTip",
    "TempToolTip",
    "TextToolTip",
    "UrlLabel",
    "buttons",
    "meters",
]
