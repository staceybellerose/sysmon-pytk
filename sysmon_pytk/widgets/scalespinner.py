# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Combination of a Scale and Spinbox.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from ..style_manager import StyleManager

if TYPE_CHECKING:
    from tkinter import BaseWidget, Variable

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-arguments, too-many-ancestors


class ScaleSpinner(ttk.Frame):
    """
    Combination of a Scale and Spinbox, with an optional Label.

    Attributes
    ----------
    variable : Variable
        The control variable which maintains the selected value.
    as_int : bool
        A flag indicating whether to round the values from the `Scale`.
    scale : Scale
        The `Scale` widget managed by this widget.
    spinbox : Spinbox
        The `Spinbox` widget managed by this widget.
    """

    def __init__(
            self, parent: BaseWidget, variable: Variable, *,
            text: str | None = None, length: int = 100, from_: float = 0,
            to: float = 100, as_int: bool = False, **kwargs
    ) -> None:
        """
        Construct a frame containing a Scale, a Spinbox, and an optional Label.

        Parameters
        ----------
        parent : BaseWidget
            The parent widget.
        variable : Variable
            The control variable which maintains the selected value.
        text : str, optional
            The text to display as a `Label`.
        length : int, default: 100
            The length of the `Scale` widget.
        from_ : float, default: 0.0
            The smallest value allowed for the `Scale` and `Spinbox`.
        to : float, default: 100.0
            The largest value allowed for the `Scale` and `Spinbox`.
        as_int : bool, default: False
            A flag indicating whether to round the values from the `Scale`.
        """
        super().__init__(parent, **kwargs)
        self.variable = variable
        self.as_int = as_int
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        base_font = StyleManager.get_base_font()
        if text is not None:
            ttk.Label(
                self, text=text, anchor=tk.W, font=base_font
            ).grid(row=0, column=0, sticky=tk.NSEW)
        self.scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, length=length, from_=from_, to=to,
            style="Tick.TScale"
        )
        self.scale.grid(row=0, column=1, pady=10, padx=10, sticky=tk.NSEW)
        self.scale.set(variable.get())
        self.spinbox = ttk.Spinbox(
            self, textvariable=variable, from_=from_, to=to,
            width=len(f"{to}")+3, state="readonly", font=base_font,
            command=self.update_from_spinbox
        )
        self.spinbox.grid(row=0, column=2, sticky=tk.EW)
        self.scale.configure(command=self.update_from_scale)

    def update_from_spinbox(self) -> None:
        """
        Update font size from spinbox.
        """
        self.scale.set(self.variable.get())

    def update_from_scale(self, size: str) -> None:
        """
        Update font size from scale widget.
        """
        self.variable.set(round(float(size)) if self.as_int else float(size))
        self.spinbox.selection_clear()
