# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Hovering tooltip.
"""

import tkinter as tk
from tkinter import BaseWidget, Event, ttk
from typing import Optional

from .._common import INTERNAL_PAD


class ToolTip:
    """
    Display a hovering tooltip while the mouse is over a given widget.

    Attributes
    ----------
    tooltip : tk.Toplevel
        The actual tooltip popup.
    parent : BaseWidget
        The parent widget, which will host the tooltip.
    text : str
        The text to display in the tooltip.
    """

    def __init__(self, parent: BaseWidget, text: str = ""):
        """
        Construct a tooltip.

        Parameters
        ----------
        parent : BaseWidget
            The parent widget, which will host the tooltip.
        text : str
            The text to display in the tooltip.
        """
        self.tooltip: Optional[tk.Toplevel] = None
        self.parent = parent
        self.text = text
        self.parent.bind("<Enter>", self.on_enter)
        self.parent.bind("<Motion>", self.on_move)
        self.parent.bind("<Leave>", self.on_leave)

    def on_enter(self, event: Event):
        """
        Handle the event when pointer enters the widget.
        """
        self.tooltip = tk.Toplevel()
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
        ttk.Label(
            self.tooltip, text=self.text, anchor=tk.CENTER,
            background="#ffd", foreground="#000"
        ).grid(ipadx=INTERNAL_PAD)

    def on_move(self, event: Event):
        """
        Handle the event when the pointer moves within the widget.
        """
        if self.tooltip:
            self.tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")

    def on_leave(self, _event: Event):
        """
        Handle the event when the pointer leaves the widget.
        """
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
