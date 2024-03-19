# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Label widget with clickable URL.
"""

import webbrowser
from tkinter import BaseWidget, Event, ttk
from typing import Any

from .tooltip import ToolTip

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-arguments, too-many-ancestors


class UrlLabel(ttk.Label):
    """
    A label containing a clickable URL.

    Attributes
    ----------
    url : str
        The URL to use when opening a web browser.
    """

    def __init__(
        self, parent: BaseWidget, text: str, url: str,
        style: str = "URL.TLabel", show_tooltip: bool = False, **kw
    ) -> None:
        """
        Construct a Label with a clickable URL.

        Parameters
        ----------
        parent : BaseWidget
            The parent widget.
        text : str
            The text to display in the label.
        url : str
            The URL to use when opening a web browser.
        style : str
            A Tcl/Tk style to use for display.
        show_tooltip : bool
            A flag to indicate whether to show a tooltip containing the URL.
        **kw : dict, optional
            Additional keyword arguments for a `Label`.
        """
        self.url = url
        cursor = "hand2" if self._has_web_protocol() else "arrow"
        super().__init__(parent, cursor=cursor, style=style, text=text, **kw)
        if show_tooltip and url:
            ToolTip(self, url)
        self.bind("<Button-1>", self.open_url)

    def open_url(self, _event: Event):
        """
        Open the widget's URL in a web browser.
        """
        if self._has_web_protocol():
            webbrowser.open_new_tab(self.url)

    def _has_web_protocol(self) -> bool:
        """
        Determine whether the string contains a web protocol (http or https).
        """
        return self.url[0:7] == "http://" or self.url[0:8] == "https://"

    @classmethod
    def has_web_protocol(cls, url: str) -> bool:
        """
        Determine whether the string contains a web protocol (http or https).
        """
        return url[0:7] == "http://" or url[0:8] == "https://"

    @classmethod
    def test_web_protocol(cls, url: str, trueval: Any, falseval: Any) -> Any:
        """
        If url uses a web protocol, return trueval; otherwise return falseval.
        """
        return trueval if cls.has_web_protocol(url) else falseval
