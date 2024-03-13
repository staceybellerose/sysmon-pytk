# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
CPU usage details modal dialog.
"""

from typing import List
import tkinter as tk
from tkinter import ttk

import psutil
from psutil._common import shwtemp

from .. import _common
from ..app_locale import _

from ._base_modal import ModalDialog


class TempDetailsDialog(ModalDialog):
    """
    Display detailed temperature readings in a modal dialog.
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
        self._readings: List[List[tk.StringVar]] = []
        ttk.Label(
            self.internal_frame, text=_("Temperature Sensors"), font=self.large_font
        ).grid(columnspan=2)
        temps = psutil.sensors_temperatures()
        row = 0
        for name, entries in temps.items():
            ttk.Label(
                self.internal_frame, text=name.upper(), anchor=tk.SW, font=self.bold_font
            ).grid(
                column=0, row=row, sticky=tk.W, ipady=_common.INTERNAL_PAD,
                padx=_common.INTERNAL_PAD
            )
            row += 1
            entryreadings: List[tk.StringVar] = []
            for count, entry in enumerate(entries):
                entryreadings.append(tk.StringVar())
                entryreadings[count].set(self._format_entry(entry))
                ttk.Label(
                    self.internal_frame, text=entry.label or name, anchor=tk.W, font=self.base_font
                ).grid(column=0, row=row, padx=_common.INTERNAL_PAD*2, sticky=tk.W)
                ttk.Label(
                    self.internal_frame, textvariable=entryreadings[count], anchor=tk.W,
                    font=self.base_font
                ).grid(column=1, row=row, padx=_common.INTERNAL_PAD, sticky=tk.W)
                row += 1
            self._readings.append(entryreadings)
        ttk.Button(
            self.internal_frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=row, column=1, sticky=tk.E,
            pady=_common.INTERNAL_PAD, padx=_common.INTERNAL_PAD
        )

    def update_screen(self):
        """
        Update the modal dialog window.
        """
        temps = psutil.sensors_temperatures()
        row = 0
        for _name, entries in temps.items():
            for count, entry in enumerate(entries):
                self._readings[row][count].set(self._format_entry(entry))
            row += 1
        self.after(_common.REFRESH_INTERVAL, self.update_screen)

    def _format_entry(self, entry: shwtemp):
        return _("{current}°C (high = {high}°C, critical = {critical}°C)").format(
            current=entry.current, high=entry.high, critical=entry.critical
        )