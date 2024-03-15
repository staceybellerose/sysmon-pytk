# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Memory usage details modal dialog.
"""

from typing import List
import tkinter as tk
from tkinter import ttk

import psutil

from .. import _common
from ..app_locale import get_translator

from ._base_modal import ModalDialog

_ = get_translator()


class MemUsageDialog(ModalDialog):
    """
    Display memory usage in a modal dialog.
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
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        self._names: List[str] = []
        self._metrics: List[tk.StringVar] = []
        self._swaps: List[str] = []
        self._swap_metrics: List[tk.StringVar] = []
        for item in mem._asdict().keys():
            self._names.append(item)
            self._metrics.append(tk.StringVar())
        for item in swap._asdict().keys():
            self._swaps.append(item)
            self._swap_metrics.append(tk.StringVar())
        self.internal_frame.columnconfigure(0, weight=1)
        self.internal_frame.columnconfigure(2, weight=4)
        self.internal_frame.columnconfigure(3, weight=1)
        ttk.Label(
            self.internal_frame, text=_("Memory Statistics"), font=self.large_font,
            anchor=tk.CENTER
        ).grid(row=0, column=0, columnspan=5, ipady=_common.INTERNAL_PAD, sticky=tk.NSEW)
        ttk.Label(
            self.internal_frame, text=_("Virtual Memory"), font=self.bold_font,
            anchor=tk.CENTER
        ).grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        ttk.Label(self.internal_frame, text="").grid(row=1, column=2)
        ttk.Label(
            self.internal_frame, text=_("Swap Memory"), font=self.bold_font,
            anchor=tk.CENTER
        ).grid(row=1, column=3, columnspan=2, sticky=tk.NSEW)
        self.internal_frame.columnconfigure(2, minsize=4*_common.INTERNAL_PAD)
        self._create_detail_widgets()
        for i in range(2, max(len(self._names), len(self._swaps))+2):
            self.internal_frame.rowconfigure(i, weight=1)
        ttk.Button(
            self.internal_frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=max(len(self._names), len(self._swaps))+3, column=3, columnspan=2,
            sticky=tk.E, padx=_common.INTERNAL_PAD/2
        )
        ttk.Sizegrip(self.internal_frame).grid(
            row=max(len(self._names), len(self._swaps))+4, column=4, sticky=tk.SE,
            padx=_common.INTERNAL_PAD/2, pady=_common.INTERNAL_PAD/2
        )

    def _create_detail_widgets(self):
        for count, name in enumerate(self._names):
            ttk.Label(
                self.internal_frame, text=name.capitalize(), anchor=tk.W,
                font=self.base_font
            ).grid(row=count+2, column=0, sticky=tk.NSEW, padx=_common.INTERNAL_PAD)
            ttk.Label(
                self.internal_frame, textvariable=self._metrics[count], anchor=tk.E,
                font=self.fixed_font
            ).grid(row=count+2, column=1, sticky=tk.NSEW, padx=_common.INTERNAL_PAD)
        for count, name in enumerate(self._swaps):
            ttk.Label(
                self.internal_frame, text=name.capitalize(), anchor=tk.W,
                font=self.base_font
            ).grid(row=count+2, column=3, sticky=tk.NSEW, padx=_common.INTERNAL_PAD)
            ttk.Label(
                self.internal_frame, textvariable=self._swap_metrics[count],
                font=self.fixed_font, anchor=tk.E
            ).grid(row=count+2, column=4, sticky=tk.NSEW, padx=_common.INTERNAL_PAD)

    def update_screen(self):
        """
        Update the modal dialog window.
        """
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        for count, item in enumerate(mem._asdict().items()):
            self._metrics[count].set(
                _common.bytes2human(item[1]) if item[0] != "percent" else f"{item[1]}%"
            )
        for count, item in enumerate(swap._asdict().items()):
            self._swap_metrics[count].set(
                _common.bytes2human(item[1]) if item[0] != "percent" else f"{item[1]}%"
            )
        self.after(_common.REFRESH_INTERVAL, self.update_screen)
