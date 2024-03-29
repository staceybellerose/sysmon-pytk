# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Modal dialogs base class.
"""

from __future__ import annotations

import tkinter as tk
from abc import ABCMeta, abstractmethod
from tkinter import ttk
from typing import TYPE_CHECKING, final

from .._common import INTERNAL_PAD
from ..app_locale import get_translator
from ..style_manager import StyleManager
from ..widgets.button_mixin import ButtonDefinition, ButtonMixin

if TYPE_CHECKING:
    from tkinter import Misc

_ = get_translator()

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-instance-attributes


class ModalDialog(ButtonMixin, tk.Toplevel, metaclass=ABCMeta):
    """
    Base class for modal dialogs.

    Attributes
    ----------
    parent : Misc, optional
        The parent widget.
    iconpath : str, optional
        The path to the icon to display in the window title bar.
    internal_frame : Frame
        A `Frame` to manage the widgets added to the dialog.
    base_font : Font
        Standard font to use for widgets.
    large_font : Font
        Large font to use for headers.
    bold_font : Font
        Bold font to use for widgets.
    fixed_font : Font
        Fixed font to use for widgets.
    _events : list[str]
        A list of event sequences to trigger after save and dismiss.
    """

    def __init__(
        self, parent: Misc | None = None, *, title: str | None = None,
        iconpath: str | None = None, class_: str = "ModalDialog"
    ) -> None:
        """
        Construct a modal dialog.

        Parameters
        ----------
        parent : Misc, optional
            The parent widget.
        title : str, optional
            The title to display in the window title bar.
        iconpath : str, optional
            The path to the icon to display in the window title bar.
        class_ : str, default: "ModalDialog"
            The class name of this modal dialog, used with the option database
            for styling.
        """
        super().__init__(parent, class_=class_)
        self.parent = parent
        self.iconpath = iconpath
        self._events: list[str] = []
        self.title(title)
        if self.iconpath is not None:
            self.iconphoto(False, tk.PhotoImage(file=self.iconpath))
        self.internal_frame = ttk.Frame(self)
        self.internal_frame.grid(sticky=tk.NSEW)
        self.load_fonts()
        self.bind_events()
        self.create_widgets()
        self.update_screen()
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.make_modal()
        self.wait_window()

    @final
    def load_fonts(self) -> None:
        """
        Load the standard fonts from the StyleManager.
        """
        self.base_font = StyleManager.get_base_font()
        self.large_font = StyleManager.get_large_font()
        self.bold_font = StyleManager.get_bold_font()
        self.fixed_font = StyleManager.get_fixed_font()

    @final
    def bind_events(self) -> None:
        """
        Bind window events.
        """
        self.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.bind("<KeyPress-Escape>", self.dismiss)
        self.bind("<KeyPress-Return>", self.save_and_dismiss)
        self.bind("<KeyPress-KP_Enter>", self.save_and_dismiss)

    @final
    def make_modal(self) -> None:
        """
        Make this behave like a modal window.
        """
        self.transient(self.parent)  # type: ignore[arg-type]
        self.wait_visibility()
        self.grab_set()
        self.minsize(self.winfo_width(), self.winfo_height())

    @final
    def dismiss(self, *_args) -> None:
        """
        Dismiss the modal dialog.

        This should be bound to Cancel and Close buttons in subclasses.
        """
        self.grab_release()
        self.destroy()

    @final
    def save_and_dismiss(self, *_args) -> None:
        """
        Save what was entered in the modal dialog and dismiss it.

        This should be bound to OK and Save buttons in subclasses.
        """
        self.on_save()
        self.dismiss()
        if self.parent:
            for event in self._events:
                self.parent.event_generate(event)

    @final
    def save_dismiss_event(self, event_str: str) -> None:
        """
        Accumulate a list of events to trigger on dismissal when saving.
        """
        if event_str not in self._events:
            self._events.append(event_str)

    @final
    def add_close_button(self) -> None:
        """
        Add a Close button to the bottom row of the modal dialog.
        """
        buttons = [
            ButtonDefinition(text=_("Close"), command=self.dismiss),
        ]
        self.add_buttons(self.internal_frame, buttons=buttons, default=0)

    @final
    def add_ok_cancel_buttons(self) -> None:
        """
        Add OK and Cancel buttons to the bottom row of the modal dialog.
        """
        buttons = [
            ButtonDefinition(text=_("Cancel"), command=self.dismiss),
            ButtonDefinition(text=_("OK"), command=self.save_and_dismiss),
        ]
        self.add_buttons(self.internal_frame, buttons=buttons, default=1)

    @final
    def add_sizegrip(self) -> None:
        """
        Add a Sizegrip widget to the bottom row of the modal dialog.
        """
        max_columns, max_rows = self.internal_frame.grid_size()
        ttk.Sizegrip(self.internal_frame).grid(
            row=max_rows, column=max_columns-1, sticky=tk.SE, padx=INTERNAL_PAD/2,
            pady=INTERNAL_PAD/2
        )

    @abstractmethod
    def on_save(self) -> None:
        """
        Save what was entered in the modal dialog.
        """

    @abstractmethod
    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """

    @abstractmethod
    def update_screen(self) -> None:
        """
        Update the modal dialog window.
        """
