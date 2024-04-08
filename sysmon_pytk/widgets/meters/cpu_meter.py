# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Self-updating CPU Meter widget.
"""

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-ancestors

from __future__ import annotations

from typing import TYPE_CHECKING

import psutil

from ... import modals
from ...app_locale import get_translator
from ...file_utils import get_full_path
from .updating_meter import UpdatingMeter

if TYPE_CHECKING:
    from tkinter import Misc

_ = get_translator()


class CpuMeter(UpdatingMeter):
    """
    A Meter to monitor CPU usage.
    """

    def __init__(
        self, parent: Misc, *, width: int = 300, height: int = 225
    ) -> None:
        """
        Construct a self-updating meter to monitor CPU usage.

        Parameters
        ----------
        parent : Misc
            The parent widget.
        width : int
            The width of the widget.
        height : int
            The height of the widget.
        """
        super().__init__(
            parent, width=width, height=height, min_value=0, max_value=100,
            label=_("CPU Usage"), unit="%", divisions=10, yellow=15, red=15,
            blue=0
        )
        self.add_tooltip(_("Click for per-CPU usage"))

    def is_clickable(self) -> bool:
        """
        CPU Meter is only clickable if more than one CPU/core is present.
        """
        return psutil.cpu_count() > 1

    def get_value(self) -> float:
        """
        Get the value that should update the meter.
        """
        return psutil.cpu_percent(interval=None)

    def on_click(self, *_args) -> None:
        """
        Open CPU Details.
        """
        app_title = self.get_app_title()
        modals.CpuDialog(
            self, title=_("{} :: CPU Details").format(app_title),
            iconpath=get_full_path("images/icon.png")
        )
