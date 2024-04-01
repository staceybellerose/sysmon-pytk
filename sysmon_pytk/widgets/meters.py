# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Various Meter widgets.
"""

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-ancestors

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, final

import psutil

from .._common import DISK_ALERT_LEVEL, DISK_WARN_LEVEL, REFRESH_INTERVAL, cpu_temp
from ..app_locale import get_translator
from ..file_utils import get_full_path
from ..modals import CpuDialog, DiskUsageDialog, MemUsageDialog, TempDetailsDialog
from .meter import Meter
from .tooltip import ToolTip

if TYPE_CHECKING:
    from tkinter import BaseWidget

_ = get_translator()


class UpdatingMeter(Meter):
    """
    A Meter that can update itself.
    """

    def __init__(
        self, parent: BaseWidget, *, width: int = 300, height: int = 225, **kw
    ) -> None:
        super().__init__(
            parent, width=width, height=height, **kw
        )
        self._update_job: str | None = None
        self.bind("<<ThemeChanged>>", self._update_theme)
        self.bind("<Destroy>", self.on_destroy)
        if self.is_clickable():
            self.bind("<Button-1>", self.on_click)
            self.configure(cursor="hand2")
        self.update_widget()

    def _update_theme(self, *_args) -> None:
        super().update_for_dark_mode()

    def is_clickable(self) -> bool:
        """
        Determine if this Meter is clickable.
        """
        return True

    def get_app_title(self) -> str:
        """
        Get the window title, based on a widget.
        """
        return self.winfo_toplevel().title()

    def on_destroy(self, *_args) -> None:
        """
        Cancel the update job when widget is destroyed.
        """
        if self._update_job is not None:
            self.after_cancel(self._update_job)
            self._update_job = None

    @abstractmethod
    def on_click(self, *args) -> None:
        """
        Handle a click event.
        """

    @abstractmethod
    def get_value(self) -> float:
        """
        Get the value that should update the meter.
        """

    @final
    def add_tooltip(self, text: str) -> None:
        """
        Add a ToolTip to the Meter.

        This method should be called by subclasses which wish to display
        a ToolTip when the mouse is hovering over the widget. It should be
        called at the end of `__init__`.
        """
        if self.is_clickable():
            ToolTip(self, text)

    @final
    def update_widget(self) -> None:
        """
        Update the Meter.
        """
        self.set_value(self.get_value())
        self._update_job = self.after(REFRESH_INTERVAL, self.update_widget)


class CpuMeter(UpdatingMeter):
    """
    A Meter to monitor CPU usage.
    """

    def __init__(
        self, parent: BaseWidget, *, width: int = 300, height: int = 225
    ) -> None:
        super().__init__(
            parent, width=width, height=height, min_value=0, max_value=100,
            label=_("CPU Usage"), unit="%", divisions=10, yellow=15, red=15,
            blue=0
        )
        self.add_tooltip(_("Click for per-CPU usage"))

    def is_clickable(self) -> bool:
        """
        CPU Meter is only clicksble if more than one CPU/core is present.
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
        CpuDialog(
            self, title=_("{} :: CPU Details").format(app_title),
            iconpath=get_full_path("images/icon.png")
        )


class TempMeter(UpdatingMeter):
    """
    A Meter to monitor CPU temperature.
    """

    def __init__(
        self, parent: BaseWidget, *, width: int = 300, height: int = 225
    ) -> None:
        super().__init__(
            parent, width=width, height=height, min_value=0, max_value=100,
            label=_("Temperature"), unit="°C", divisions=10, yellow=15, red=15,
            blue=15
        )
        self.add_tooltip(_("Click for detailed temperature readings"))

    def get_value(self) -> float:
        """
        Get the value that should update the meter.
        """
        return cpu_temp()

    def on_click(self, *_args) -> None:
        """
        Open Temperature Details.
        """
        app_title = self.get_app_title()
        TempDetailsDialog(
            self,
            title=_("{} :: Temperature Details").format(app_title),
            iconpath=get_full_path("images/icon.png")
        )


class RamMeter(UpdatingMeter):
    """
    A Meter to monitor RAM usage.
    """

    def __init__(
        self, parent: BaseWidget, *, width: int = 300, height: int = 225
    ) -> None:
        super().__init__(
            parent, width=width, height=height, min_value=0, max_value=100,
            label=_("RAM Usage"), unit="%", divisions=10, yellow=15, red=15,
            blue=0
        )
        self.add_tooltip(_("Click for detailed memory statistics"))

    def get_value(self) -> float:
        """
        Get the value that should update the meter.
        """
        return psutil.virtual_memory().percent

    def on_click(self, *_args) -> None:
        """
        Open Memory Usage.
        """
        app_title = self.get_app_title()
        MemUsageDialog(
            self, title=_("{} :: Memory Usage").format(app_title),
            iconpath=get_full_path("images/icon.png")
        )


class DiskMeter(UpdatingMeter):
    """
    A Meter to monitor disk usage.
    """

    def __init__(
        self, parent: BaseWidget, *, width: int = 300, height: int = 225
    ) -> None:
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
        DiskUsageDialog(
            self, title=_("{} :: Disk Usage").format(app_title),
            iconpath=get_full_path("images/icon.png")
        )
