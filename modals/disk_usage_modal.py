# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Disk usage details modal dialog.
"""

from typing import List
import tkinter as tk
from tkinter import ttk, font

import psutil

import _common
from app_locale import _

from ._base_modal import ModalDialog

class DiskUsageDialog(ModalDialog):
    """
    Display disk usage in a modal dialog.
    """

    def on_save(self):
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.

        This dialog does not require additional styles.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self._diskmounts: List[str] = []
        self._diskusages: List[tk.IntVar] = []
        self._diskusagefmts: List[tk.StringVar] = []
        for part in psutil.disk_partitions():
            self._diskmounts.append(part.mountpoint)
            self._diskusages.append(tk.IntVar())
            self._diskusagefmts.append(tk.StringVar())
        base_font = font.nametofont("TkDefaultFont")
        large_font = _common.modify_named_font(
            "TkDefaultFont", size=base_font.actual()["size"]+4
        )
        fixed_font = font.nametofont("TkFixedFont")
        ttk.Label(
            self.internal_frame, text=_("Disk Usage"), font=large_font
        ).grid(columnspan=2)
        self._disklabels: List[ttk.Label] = []
        for col, mountpoint in enumerate(self._diskmounts):
            ttk.Label(
                self.internal_frame, text=mountpoint, anchor=tk.SW,
                font=base_font
            ).grid(row=2*col + 1, column=0, sticky=tk.W)
            ttk.Progressbar(
                self.internal_frame, length=300, orient=tk.HORIZONTAL,
                variable=self._diskusages[col]
            ).grid(row=2*col + 2, column=0)
            usagelabel = ttk.Label(
                self.internal_frame, textvariable=self._diskusagefmts[col],
                anchor=tk.E, font=fixed_font
            )
            self._disklabels.append(usagelabel)
            usagelabel.grid(
                row=2*col + 2, column=1, padx=_common.INTERNAL_PAD, sticky=tk.E
            )
        ttk.Button(
            self.internal_frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=2*len(self._diskmounts) + 2, column=1, sticky=tk.E,
            pady=_common.INTERNAL_PAD, padx=_common.INTERNAL_PAD
        )

    def reset(self):
        """
        Reset the dialog.
        """
        self.internal_frame.destroy()
        self.create_widgets()
        self.update_screen()

    def update_screen(self):
        """
        Update the modal dialog window.
        """
        # update the mount points
        for part in psutil.disk_partitions():
            if part.mountpoint not in self._diskmounts:
                # newly mounted drive discovered - reset the widget
                self.reset()
                return
        # process the mount points
        for col, mountpoint in enumerate(self._diskmounts):
            try:
                usage = psutil.disk_usage(mountpoint).percent
                self._diskusages[col].set(round(usage))
                self._diskusagefmts[col].set(_common.disk_usage(mountpoint))
                if usage >= _common.DISK_ALERT_LEVEL:
                    style_name = "Alert.TLabel"
                elif usage >= _common.DISK_WARN_LEVEL:
                    style_name = "Warn.TLabel"
                else:
                    style_name = "Safe.TLabel"
                self._disklabels[col].configure(style=style_name)
            except FileNotFoundError:
                # disk was unmounted, reset the widget
                self.reset()
                return
        self.after(_common.REFRESH_INTERVAL, self.update_screen)
