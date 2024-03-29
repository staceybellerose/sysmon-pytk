# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Standard Edit Menu with Cut/Copy/Paste/Select All items.
"""

from __future__ import annotations

import dataclasses
import tkinter as tk

from ..app_locale import get_translator
from ..file_utils import get_full_path

_ = get_translator()


@dataclasses.dataclass
class EditMenuImages:
    """
    Images used for the Edit Menu.
    """

    cut: tk.PhotoImage
    copy: tk.PhotoImage
    paste: tk.PhotoImage
    select_all: tk.PhotoImage


class EditMenu(tk.Menu):
    """
    Standard Edit Menu with Cut/Copy/Paste/Select All items.

    Attributes
    ----------
    images : EditMenuImages
        A collection of images needed for the menu.
    """

    def __init__(self, master: tk.Text, **kwarg) -> None:
        self.master: tk.Text = master
        super().__init__(master, **kwarg)
        self.images = EditMenuImages(
            cut=tk.PhotoImage(file=get_full_path("images/edit-cut.png")),
            copy=tk.PhotoImage(file=get_full_path("images/edit-copy.png")),
            paste=tk.PhotoImage(file=get_full_path("images/edit-paste.png")),
            select_all=tk.PhotoImage(file=get_full_path("images/edit-select-all.png"))
        )
        self.add_command(
            label=("Cut"), command=self._cut, accelerator=_("Ctrl+X"),
            compound=tk.LEFT, image=self.images.cut
        )
        self.add_command(
            label=("Copy"), command=self._copy, accelerator=_("Ctrl+C"),
            compound=tk.LEFT, image=self.images.copy
        )
        self.add_command(
            label=("Paste"), command=self._paste, accelerator=_("Ctrl+V"),
            compound=tk.LEFT, image=self.images.paste
        )
        self.add_separator()
        self.add_command(
            label=("Select All"), command=self._select_all,
            accelerator=_("Ctrl+A"), compound=tk.LEFT, image=self.images.select_all
        )
        self.master.bind("<Button-3>", self._show_popup)
        self.master.bind("<Control-X>", self._cut)
        self.master.bind("<Control-C>", self._copy)
        self.master.bind("<Control-V>", self._paste)
        self.master.bind("<Control-A>", self._select_all)

    def _show_popup(self, event: tk.Event) -> None:
        if self.focus_get() != self:
            self.focus_set()
        if self.master.cget("state") == tk.DISABLED:
            self.entryconfigure(("Cut"), state=tk.DISABLED)
            self.entryconfigure(("Paste"), state=tk.DISABLED)
        else:
            self.entryconfigure(("Cut"), state=tk.NORMAL)
            self.entryconfigure(("Paste"), state=tk.NORMAL)
        self.tk_popup(event.x_root, event.y_root, 0)

    def _cut(self, *_args) -> None:
        if self.master.cget("state") == tk.NORMAL:
            self.master.event_generate("<<Cut>>")

    def _copy(self, *_args) -> None:
        self.master.event_generate("<<Copy>>")

    def _paste(self, *_args) -> None:
        if self.master.cget("state") == tk.NORMAL:
            self.master.event_generate("<<Paste>>")

    def _select_all(self, *_args) -> None:
        self.master.tag_add(tk.SEL, "1.0", "end-1c")
