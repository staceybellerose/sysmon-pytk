# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Disk usage details modal dialog.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

import psutil

from .. import _common
from ..app_locale import get_translator
from ._base_modal import ModalDialog

if TYPE_CHECKING:
    from tkinter import Misc

_ = get_translator()


class DiskUsageDialog(ModalDialog):
    """
    Display disk usage in a modal dialog.
    """

    def __init__(
        self, parent: Misc | None = None, *, title: str | None = None,
        iconpath: str | None = None, class_: str = "ModalDialog"
    ) -> None:
        self._update_job: str | None = None
        super().__init__(parent, title=title, iconpath=iconpath, class_=class_)

    def on_save(self) -> None:
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self._diskmounts: list[str] = []
        self._diskusages: list[tk.IntVar] = []
        self._diskusagefmts: list[tk.StringVar] = []
        self._disklabels: list[ttk.Label] = []
        for part in psutil.disk_partitions():
            self._diskmounts.append(part.mountpoint)
            self._diskusages.append(tk.IntVar())
            self._diskusagefmts.append(tk.StringVar())
        self.internal_frame.columnconfigure(0, weight=1)
        ttk.Label(
            self.internal_frame, text=_("Disk Usage"), font=self.large_font,
            anchor=tk.CENTER
        ).grid(columnspan=2, sticky=tk.NSEW, ipady=_common.INTERNAL_PAD)
        self._create_mount_widgets()
        for i in range(1, 2*len(self._diskmounts) + 1):
            self.internal_frame.rowconfigure(i, weight=1)
        self.add_close_button()
        self.add_sizegrip()

    def _create_mount_widgets(self) -> None:
        for col, mountpoint in enumerate(self._diskmounts):
            ttk.Label(
                self.internal_frame, text=mountpoint, anchor=tk.SW,
                font=self.base_font
            ).grid(row=2*col + 1, column=0, sticky=tk.NSEW)
            ttk.Progressbar(
                self.internal_frame, length=300, orient=tk.HORIZONTAL,
                variable=self._diskusages[col]
            ).grid(row=2*col + 2, column=0, sticky=tk.NSEW)
            usagelabel = ttk.Label(
                self.internal_frame, textvariable=self._diskusagefmts[col],
                anchor=tk.E, font=self.fixed_font
            )
            self._disklabels.append(usagelabel)
            usagelabel.grid(
                row=2*col + 2, column=1, padx=_common.INTERNAL_PAD,
                sticky=tk.NSEW
            )

    def reset(self) -> None:
        """
        Reset the dialog.
        """
        if self._update_job is not None:
            self.after_cancel(self._update_job)
            self._update_job = None
        self.internal_frame.destroy()
        self.create_widgets()
        self.update_screen()

    def check_mount_points(self) -> bool:
        """
        Check to see if any additional mount points have appeared.
        """
        return any(
            part.mountpoint not in self._diskmounts for part in psutil.disk_partitions()
        )

    def update_screen(self) -> None:
        """
        Update the modal dialog window.
        """
        if self.check_mount_points():
            self.reset()
            return
        # process the mount points
        try:
            for col, mountpoint in enumerate(self._diskmounts):
                usage = psutil.disk_usage(mountpoint).percent
                self._diskusages[col].set(round(usage))
                self._diskusagefmts[col].set(_common.disk_usage(mountpoint))
                self._disklabels[col].configure(style=self._get_alert_style(usage))
        except FileNotFoundError:
            # disk was unmounted, reset the widget
            self.reset()
            return
        self._update_job = self.after(_common.REFRESH_INTERVAL, self.update_screen)

    @classmethod
    def _get_alert_style(cls, usage: float) -> str:
        if usage >= _common.DISK_ALERT_LEVEL:
            return "Alert.TLabel"
        if usage >= _common.DISK_WARN_LEVEL:
            return "Warn.TLabel"
        return "Safe.TLabel"
