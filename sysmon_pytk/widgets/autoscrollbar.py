# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
AutoScrollbar widget.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import TclError, ttk
from typing import Any, Literal, TypeVar

from typing_extensions import Self

ScrollableWidget = TypeVar(
    "ScrollableWidget", tk.Canvas, tk.Listbox, tk.Text, ttk.Treeview
)


class AutoScrollbar(ttk.Scrollbar):  # pylint: disable=too-many-ancestors
    """
    A scrollbar that automatically removes itself when not needed.
    """

    def set(self, first: Any, last: Any) -> None:  # noqa: ANN401
        """
        Set the fractional values of the slider position.

        Upper and lower ends are values between 0 and 1.
        """
        if float(first) <= 0 and float(last) >= 1:
            self.grid_remove()
        else:
            self.grid()
        super().set(first, last)

    def pack(self, **_kwargs):  # noqa: ANN201
        """
        Disable pack for this widget.
        """
        msg = "cannot use pack with this widget"
        raise TclError(msg)

    def place(self, **_kwargs):  # noqa: ANN201
        """
        Disable place for this widget.
        """
        msg = "cannot use place with this widget"
        raise TclError(msg)

    @classmethod
    def add_to_widget(
        cls, widget: ScrollableWidget, orient: Literal["horizontal", "vertical"],
        **kwargs
    ) -> Self:
        """
        Add a scrollbar to a scrollable widget.
        """
        scroller = cls(widget.master, orient=orient, **kwargs)
        if orient == "horizontal":
            scroller.config(command=widget.xview)
            widget.config(xscrollcommand=scroller.set)
        else:
            scroller.config(command=widget.yview)
            widget.config(yscrollcommand=scroller.set)
        return scroller
