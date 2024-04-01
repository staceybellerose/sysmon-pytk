# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Scrollable Text Widget with standard Edit popup menu.
"""

from __future__ import annotations

import tkinter as tk
import webbrowser
from tkinter import font, ttk

from ..app_locale import get_translator
from ..style_manager import StyleManager
from .autoscrollbar import AutoScrollbar
from .edit_menu import EditMenu

_ = get_translator()

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-ancestors


class ScrollingText(tk.Text):
    """
    Scrollable Text Widget with standard Edit popup menu.

    Attributes
    ----------
    frame : Frame
        The frame which holds this widget and its accompanying AutoScrollbar.

    Notes
    -----
    This Text widget is configured with several standard tags.
        center : Center the tagged text.
        left : Left justify the tagged text.
        right : Right justify the tagged text.
        large : apply the large font to the tagged text.
        bold : apply the bold font to the tagged text.
        fixed : apply the fixed font to the tagged text.
        link : treat the tagged text as a clickable link.
        linkurl : follows a link tag, and contains the url to open - hidden text.

    To use links, insert a `link` tag with the clickable link text, and then
    insert a `linkurl` tag containing the url to open for the previous link
    text. The `linkurl` text will be hidden, but accessible when the user
    clicks on the link. When the user clicks, the text position of the click
    will be determined, from that position, the text will be searched for the
    next occurrence of a `linkurl` tag, and that url will be opened.
    """

    def __init__(self, master: tk.Misc | None = None, **kwargs) -> None:
        self.frame = ttk.Frame(master)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        super().__init__(self.frame, **kwargs)
        self.grid(row=0, column=0, sticky=tk.NSEW)
        self._configure_tags()
        AutoScrollbar.add_to_widget(self, orient=tk.VERTICAL).grid(
            row=0, column=1, sticky=tk.NS
        )
        EditMenu(
            self, activeborderwidth=0,  # relief=tk.FLAT,
            background=StyleManager.test_dark_mode("#444444", "#dddddd"),
            foreground=StyleManager.test_dark_mode("#ffffff", "#000000"),
            font=font.nametofont("TkMenuFont")
        )

    def get_frame(self) -> ttk.Frame:
        """
        Get the containing frame.
        """
        return self.frame

    def _configure_tags(self) -> None:
        """
        Configure the standard tags for the Text widget.
        """
        self.tag_configure("center", justify="center")
        self.tag_configure("left", justify="left")
        self.tag_configure("right", justify="right")
        self.tag_configure("large", font=StyleManager.get_large_font())
        self.tag_configure("bold", font=StyleManager.get_bold_font())
        self.tag_configure("fixed", font=StyleManager.get_fixed_font())
        self.tag_configure(
            "link", foreground="#007fff", selectforeground="#007fff",
            selectbackground="#cccccc"
        )
        self.tag_configure("linkurl", elide=True)  # hide the urls from display
        self.tag_bind("link", "<Enter>", self.show_hand_cursor)
        self.tag_bind("link", "<Leave>", self.hide_hand_cursor)
        self.tag_bind("link", "<Button-1>", self.open_link)
        # TODO add "Open in Browser" edit menu item when hovering over link

    def show_hand_cursor(self, event: tk.Event[tk.Text]) -> None:
        """
        Change the mouse cursor to a "hand", indicating a clickable link.
        """
        event.widget.configure(cursor="hand2")

    def hide_hand_cursor(self, event: tk.Event[tk.Text]) -> None:
        """
        Change the mouse cursor to its standard form, no longer indicating a link.
        """
        event.widget.configure(cursor="")

    def open_link(self, event: tk.Event[tk.Text]) -> None:
        """
        Open the clicked link in a web browser.
        """
        click_position = f"@{event.x},{event.y}"
        tag_range = event.widget.tag_nextrange("linkurl", click_position)
        webbrowser.open_new_tab(event.widget.get(*tag_range))
