# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
CPU usage details modal dialog.
"""

from typing import List
import tkinter as tk
from tkinter import ttk

import psutil

import _common
from tkmeter import Meter
from app_locale import _

from ._base_modal import ModalDialog


class CpuDialog(ModalDialog):
    """
    Display individual CPU core usage details in a modal dialog.

    Attributes
    ----------
    cpu_count : int
        The number of logical CPUs in the system.
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
        self.cpu_count = psutil.cpu_count()
        cpu_model = _common.get_processor_name()
        max_columns = 4
        ttk.Label(
            self.internal_frame, text=cpu_model, font=self.large_font
        ).grid(columnspan=max_columns)
        ttk.Label(
            self.internal_frame, text=_("per-core CPU Usage"), font=self.large_font
        ).grid(columnspan=max_columns, row=1)
        row = 2
        col = 0
        self._meters: List[Meter] = []
        for core in range(self.cpu_count):
            meter = Meter(
                self.internal_frame, width=220, height=165, unit="%",
                label=_("CPU #{}").format(core)
            )
            meter.grid(row=row, column=col, sticky=tk.N, ipady=_common.INTERNAL_PAD)
            self._meters.append(meter)
            col += 1
            if col == max_columns:
                col = 0
                row += 1
        row += 1
        ttk.Label(
            self.internal_frame, text=_("per-core CPU Frequency (in MHz)"),
            font=self.large_font
        ).grid(columnspan=max_columns, row=row)
        row += 1
        self._freqmeters: List[Meter] = []
        freqs = psutil.cpu_freq(percpu=True)
        for core in range(self.cpu_count):
            meter = Meter(
                self.internal_frame, width=220, height=165, unit="",
                label=_("CPU #{}").format(core),
                min_value=freqs[core].min, max_value=freqs[core].max  # type: ignore
            )
            meter.grid(row=row, column=col, sticky=tk.N, ipady=_common.INTERNAL_PAD)
            self._freqmeters.append(meter)
            col += 1
            if col == max_columns:
                col = 0
                row += 1
        row += 1
        ttk.Button(
            self.internal_frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=row, column=1, sticky=tk.E, columnspan=max_columns,
            pady=_common.INTERNAL_PAD, padx=_common.INTERNAL_PAD
        )

    def update_screen(self):
        """
        Update the modal dialog window.
        """
        usage = psutil.cpu_percent(interval=None, percpu=True)
        for core in range(self.cpu_count):
            self._meters[core].set_value(usage[core])
        freqs = psutil.cpu_freq(percpu=True)
        for core in range(self.cpu_count):
            self._freqmeters[core].set_value(freqs[core].current)
        self.after(_common.REFRESH_INTERVAL, self.update_screen)
