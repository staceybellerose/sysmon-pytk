# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Updating Meter widget base class.
"""

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-ancestors

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, final

from ..._common import REFRESH_INTERVAL
from ...app_locale import get_translator
from ..meter import Meter
from ..tooltip import ToolTip

if TYPE_CHECKING:
    from tkinter import Misc

_ = get_translator()


class UpdatingMeter(Meter):
    """
    A Meter that can update itself.
    """

    def __init__(
        self, parent: Misc, *, width: int = 300, height: int = 225, **kw
    ) -> None:
        """
        Construct a self-updating meter.

        Parameters
        ----------
        parent : Misc
            The parent widget.
        width : int
            The width of the meter widget.
        height : int
            The height of the meter widget.
        **kw : dict, optional
            Arguments to pass to parent Meter class.
        """
        super().__init__(
            parent, width=width, height=height, **kw
        )
        self._update_job: str | None = None
        self.bind("<<ThemeChanged>>", self._update_theme)
        self.bind("<Destroy>", self.on_destroy)
        if self.is_clickable():
            self.bind("<Button-1>", self.on_click)
            self.configure(cursor="hand2")
        self.update_widget()

    def _update_theme(self, *_args) -> None:
        super().update_for_dark_mode()

    def is_clickable(self) -> bool:
        """
        Determine if this Meter is clickable.
        """
        return True

    def get_app_title(self) -> str:
        """
        Get the window title, based on a widget.
        """
        return self.winfo_toplevel().title()

    def on_destroy(self, *_args) -> None:
        """
        Cancel the update job when widget is destroyed.
        """
        if self._update_job is not None:
            self.after_cancel(self._update_job)
            self._update_job = None

    @abstractmethod
    def on_click(self, *args) -> None:
        """
        Handle a click event.
        """

    @abstractmethod
    def get_value(self) -> float:
        """
        Get the value that should update the meter.
        """

    @final
    def add_tooltip(self, text: str) -> None:
        """
        Add a ToolTip to the Meter.

        This method should be called by subclasses which wish to display
        a ToolTip when the mouse is hovering over the widget. It should be
        called at the end of `__init__`.
        """
        if self.is_clickable():
            ToolTip(self, text)

    @final
    def update_widget(self) -> None:
        """
        Update the Meter.
        """
        self.set_value(self.get_value())
        self._update_job = self.after(REFRESH_INTERVAL, self.update_widget)
