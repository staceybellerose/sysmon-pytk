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
from ..widgets import Meter
from ._base_modal import ModalDialog

if TYPE_CHECKING:
    from tkinter import Misc

_ = get_translator()


class CpuDialog(ModalDialog):
    """
    Display individual CPU core usage details in a modal dialog.

    Attributes
    ----------
    cpu_count : int
        The number of logical CPUs in the system.
    """

    MAX_COLUMNS = 4

    def __init__(
        self, parent: Misc | None = None, *, title: str | None = None,
        iconpath: str | None = None, class_: str = "ModalDialog"
    ) -> None:
        self._max_used_column = 0
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
        self.cpu_count = psutil.cpu_count()
        self.internal_frame.columnconfigure(0, weight=1)
        self.internal_frame.columnconfigure(1, weight=1)
        self.internal_frame.columnconfigure(2, weight=1)
        self.internal_frame.columnconfigure(3, weight=1)
        self._meter_rows: list[int] = []
        self._meters: list[Meter] = []
        self._freqmeters: list[Meter] = []
        ttk.Label(
            self.internal_frame, text=_common.get_processor_name(),
            font=self.large_font, anchor=tk.CENTER
        ).grid(columnspan=self.MAX_COLUMNS, sticky=tk.EW, ipady=_common.INTERNAL_PAD)
        ttk.Label(
            self.internal_frame, text=_("per-core CPU Usage"),
            font=self.large_font, anchor=tk.CENTER
        ).grid(columnspan=self.MAX_COLUMNS, row=1, sticky=tk.EW)
        row = 2
        row = self._create_usage_widgets(row) + 1
        ttk.Label(
            self.internal_frame, text=_("per-core CPU Frequency (in MHz)"),
            font=self.large_font, anchor=tk.CENTER
        ).grid(columnspan=self.MAX_COLUMNS, row=row, sticky=tk.EW)
        row = self._create_freq_widgets(row+1) + 1
        for meter_row in self._meter_rows:
            self.internal_frame.rowconfigure(meter_row, weight=1)
        self.add_close_button()
        self.add_sizegrip()

    def _create_usage_widgets(self, start_row: int) -> int:
        row = start_row
        col = 0
        for core in range(self.cpu_count):
            meter = Meter(
                self.internal_frame, width=220, height=165, unit="%",
                label=_("CPU #{}").format(core)
            )
            meter.grid(row=row, column=col, sticky=tk.NSEW, ipady=_common.INTERNAL_PAD)
            if row not in self._meter_rows:
                self._meter_rows.append(row)
            self._meters.append(meter)
            self._max_used_column = max(self._max_used_column, col)
            col += 1
            if col == self.MAX_COLUMNS:
                col = 0
                row += 1
        return row

    def _create_freq_widgets(self, start_row: int) -> int:
        row = start_row
        col = 0
        freqs = psutil.cpu_freq(percpu=True)
        for core in range(self.cpu_count):
            meter = Meter(
                self.internal_frame, width=220, height=165, unit="",
                label=_("CPU #{}").format(core),
                min_value=freqs[core].min, max_value=freqs[core].max  # type: ignore[attr-defined]
            )
            meter.grid(row=row, column=col, sticky=tk.NSEW, ipady=_common.INTERNAL_PAD)
            if row not in self._meter_rows:
                self._meter_rows.append(row)
            self._freqmeters.append(meter)
            self._max_used_column = max(self._max_used_column, col)
            col += 1
            if col == self.MAX_COLUMNS:
                col = 0
                row += 1
        return row

    def update_screen(self) -> None:
        """
        Update the modal dialog window.
        """
        usage = psutil.cpu_percent(interval=None, percpu=True)
        for core in range(self.cpu_count):
            self._meters[core].set_value(usage[core])
        freqs = psutil.cpu_freq(percpu=True)
        for core in range(self.cpu_count):
            self._freqmeters[core].set_value(freqs[core].current)  # type: ignore[attr-defined]
        self.after(_common.REFRESH_INTERVAL, self.update_screen)
