# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Self-updating Disk Meter widget.
"""

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-ancestors

from __future__ import annotations

from typing import TYPE_CHECKING

import psutil

from ... import modals
from ..._common import DISK_ALERT_LEVEL, DISK_WARN_LEVEL
from ...app_locale import get_translator
from ...file_utils import get_full_path
from .updating_meter import UpdatingMeter

if TYPE_CHECKING:
    from tkinter import Misc

_ = get_translator()


class DiskMeter(UpdatingMeter):
    """
    A Meter to monitor disk usage.
    """

    def __init__(
        self, parent: Misc, *, width: int = 300, height: int = 225
    ) -> None:
        """
        Construct a self-updating meter to monitor disk usage.

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
            label=_("Disk Usage: /"), unit="%", divisions=10, blue=0,
            red=100 - DISK_ALERT_LEVEL, yellow=DISK_ALERT_LEVEL - DISK_WARN_LEVEL
        )
        self.add_tooltip(_("Click for usage details of each mount point"))

    def get_value(self) -> float:
        """
        Get the value that should update the meter.
        """
        return psutil.disk_usage("/").percent

    def on_click(self, *_args) -> None:
        """
        Open Disk Usage.
        """
        app_title = self.get_app_title()
        modals.DiskUsageDialog(
            self, title=_("{} :: Disk Usage").format(app_title),
            iconpath=get_full_path("images/icon.png")
        )
