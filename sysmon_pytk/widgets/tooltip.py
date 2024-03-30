# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Hovering tooltip.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from .._common import INTERNAL_PAD
from ..style_manager import StyleManager

if TYPE_CHECKING:
    from tkinter import Event, Misc, Text


class ToolTip:
    """
    Display a hovering tooltip while the mouse is over a given widget.

    Attributes
    ----------
    tooltip : tk.Toplevel
        The actual tooltip popup.
    parent : Misc
        The parent widget, which will host the tooltip.
    text : str
        The text to display in the tooltip.
    """

    def __init__(self, parent: Misc, text: str = "") -> None:
        """
        Construct a tooltip.

        Parameters
        ----------
        parent : Misc
            The parent widget, which will host the tooltip.
        text : str
            The text to display in the tooltip.
        """
        self.tooltip: tk.Toplevel | None = None
        self.parent = parent
        self.text = text
        self.bind_events()

    def bind_events(self) -> None:
        """
        Bind the Enter, Leave, Motion events to the parent widget.
        """
        self.parent.bind("<Enter>", self.on_enter)
        self.parent.bind("<Motion>", self.on_move)
        self.parent.bind("<Leave>", self.on_leave)

    def on_enter(self, event: Event) -> None:
        """
        Handle the event when pointer enters the widget.
        """
        self.tooltip = tk.Toplevel(class_="ToolTip")
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
        ttk.Label(
            self.tooltip, text=self.text, font=StyleManager.get_small_font(),
            background="#ffffdd", foreground="#000000", anchor=tk.CENTER
        ).grid(ipadx=INTERNAL_PAD)

    def on_move(self, event: Event) -> None:
        """
        Handle the event when the pointer moves within the widget.
        """
        if self.tooltip:
            self.tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")

    def on_leave(self, _event: Event) -> None:
        """
        Handle the event when the pointer leaves the widget.
        """
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class TextToolTip(ToolTip):
    """
    A ToolTip subclass for use with Text widgets.

    Attributes
    ----------
    tag : str
        A tag used in the Text widget with which to link this tooltip.
    """

    def __init__(self, parent: Text, text: str = "", tag: str = "") -> None:
        self.tag = tag
        super().__init__(parent, text)

    def bind_events(self) -> None:
        """
        Bind the Enter, Leave, Motion events to the tag on the parent Text widget.
        """
        parent: Text = self.parent  # type: ignore[assignment]
        parent.tag_bind(self.tag, "<Enter>", self.on_enter, "+")
        parent.tag_bind(self.tag, "<Motion>", self.on_move, "+")
        parent.tag_bind(self.tag, "<Leave>", self.on_leave, "+")


class TempToolTip(ToolTip):
    """
    A Temporary tooltip that times out after a few seconds.
    """

    def __init__(
        self, parent: Misc, text: str = "",
        position: tuple[int, int] = (0, 0), timer_ms: int = 2000
    ) -> None:
        """
        Construct a tooltip.

        Parameters
        ----------
        parent : Misc
            The parent widget, which will host the tooltip.
        text : str
            The text to display in the tooltip.
        position : tuple[int, int]
            The (X, Y) position of the tooltip.
        timer_ms : int
            The number of milliseconds to display the tooltip.
        """
        super().__init__(parent, text)
        self.tooltip = tk.Toplevel(class_="ToolTip")
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f"+{position[0]}+{position[1]}")
        ttk.Label(
            self.tooltip, text=self.text, font=StyleManager.get_small_font(),
            background="#ffffdd", foreground="#000000", anchor=tk.CENTER
        ).grid(ipadx=INTERNAL_PAD)
        self.tooltip.after(timer_ms, self.dismiss)

    def bind_events(self) -> None:
        """
        Don't handle any events.
        """

    def dismiss(self) -> None:
        """
        Dismiss the tooltip.
        """
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
