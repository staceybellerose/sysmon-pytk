# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Memory usage details modal dialog.
"""

from typing import List
import tkinter as tk
from tkinter import ttk, font

import psutil

import _common
from app_locale import _

from ._base_modal import ModalDialog

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
        for count, item in enumerate(mem._asdict().items()):
            self._names.append(item[0])
            self._metrics.append(tk.StringVar())
        for count, item in enumerate(swap._asdict().items()):
            self._swaps.append(item[0])
            self._swap_metrics.append(tk.StringVar())
        base_font = font.nametofont("TkDefaultFont")
        large_font = _common.modify_named_font(
            "TkDefaultFont", size=base_font.actual()["size"]+4
        )
        bold_font = _common.modify_named_font(
            "TkDefaultFont", weight="bold"
        )
        fixed_font = font.nametofont("TkFixedFont")
        ttk.Label(
            self.internal_frame, text=_("Memory Statistics"), font=large_font
        ).grid(row=0, column=0, columnspan=5)
        ttk.Label(
            self.internal_frame, text=_("Virtual Memory"), font=bold_font
        ).grid(row=1, column=0, columnspan=2)
        ttk.Label(self.internal_frame, text="").grid(row=1, column=2)
        ttk.Label(
            self.internal_frame, text=_("Swap Memory"), font=bold_font
        ).grid(row=1, column=3, columnspan=2)
        self.internal_frame.columnconfigure(2, minsize=4*_common.INTERNAL_PAD)
        for count, name in enumerate(self._names):
            ttk.Label(
                self.internal_frame, text=name.capitalize(), anchor=tk.W,
                font=base_font
            ).grid(row=count+2, column=0, sticky=tk.W, padx=_common.INTERNAL_PAD)
            ttk.Label(
                self.internal_frame, textvariable=self._metrics[count], anchor=tk.E,
                font=fixed_font
            ).grid(row=count+2, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        for count, name in enumerate(self._swaps):
            ttk.Label(
                self.internal_frame, text=name.capitalize(), anchor=tk.W,
                font=base_font
            ).grid(row=count+2, column=3, sticky=tk.W, padx=_common.INTERNAL_PAD)
            ttk.Label(
                self.internal_frame, textvariable=self._swap_metrics[count],
                font=fixed_font, anchor=tk.E
            ).grid(row=count+2, column=4, sticky=tk.E, padx=_common.INTERNAL_PAD)
        ttk.Button(
            self.internal_frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=max(len(self._names), len(self._swaps))+3, column=3, columnspan=2,
            sticky=tk.E, pady=_common.INTERNAL_PAD, padx=_common.INTERNAL_PAD
        )

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
