# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
CPU usage details modal dialog.
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
    from psutil._common import shwtemp

_ = get_translator()


class TempDetailsDialog(ModalDialog):
    """
    Display detailed temperature readings in a modal dialog.
    """

    def on_save(self) -> None:
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self.internal_frame.columnconfigure(0, weight=1)
        self._readings: list[list[tk.StringVar]] = []
        ttk.Label(
            self.internal_frame, text=_("Temperature Sensors"), font=self.large_font,
            anchor=tk.CENTER
        ).grid(columnspan=2, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0))
        temps = psutil.sensors_temperatures()
        stretchy_rows = self._create_detail_widgets(temps, 1)
        for i in stretchy_rows:
            self.internal_frame.rowconfigure(i, weight=1)
        self.add_close_button()
        self.add_sizegrip()

    def _create_detail_widgets(
        self, temps: dict[str, list[shwtemp]], start_row: int
    ) -> list[int]:
        row = start_row
        stretchy_rows: list[int] = []
        for name, entries in temps.items():
            ttk.Label(
                self.internal_frame, text=name.upper(), anchor=tk.SW, font=self.bold_font
            ).grid(
                column=0, row=row, sticky=tk.NSEW, padx=_common.INTERNAL_PAD,
                columnspan=2
            )
            stretchy_rows.append(row)
            row += 1
            entryreadings: list[tk.StringVar] = []
            for count, entry in enumerate(entries):
                entryreadings.append(tk.StringVar())
                entryreadings[count].set(self._format_entry(entry))
                ttk.Label(
                    self.internal_frame, text=entry.label or name, anchor=tk.W,
                    font=self.base_font
                ).grid(column=0, row=row, padx=_common.INTERNAL_PAD*2, sticky=tk.NSEW)
                ttk.Label(
                    self.internal_frame, textvariable=entryreadings[count], anchor=tk.W,
                    font=self.base_font
                ).grid(column=1, row=row, padx=_common.INTERNAL_PAD, sticky=tk.NSEW)
                stretchy_rows.append(row)
                row += 1
            self._readings.append(entryreadings)
            ttk.Separator(self.internal_frame, orient=tk.HORIZONTAL).grid(
                column=0, columnspan=2, row=row, sticky=tk.NSEW,
                padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
            )
            row += 1
        return stretchy_rows

    def update_screen(self) -> None:
        """
        Update the modal dialog window.
        """
        temps = psutil.sensors_temperatures()
        for row, entries in enumerate(temps.values()):
            for count, entry in enumerate(entries):
                self._readings[row][count].set(self._format_entry(entry))
        self.after(_common.REFRESH_INTERVAL, self.update_screen)

    @classmethod
    def _format_entry(cls, entry: shwtemp) -> str:
        return _("{current}°C (high = {high}°C, critical = {critical}°C)").format(
            current=entry.current, high=entry.high, critical=entry.critical
        )
