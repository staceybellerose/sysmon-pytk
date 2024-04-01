# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Themed message boxes.
"""

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-arguments

from __future__ import annotations

import tkinter as tk
from contextlib import suppress
from enum import IntEnum
from tkinter import ttk
from typing import Callable

from .._common import INTERNAL_PAD
from ..app_locale import get_translator
from ..file_utils import get_full_path
from ..widgets.button_mixin import ButtonMixin, ButtonName

_ = get_translator()


class MessageBoxIcon(IntEnum):
    """
    Standard message box icons.
    """

    INFO = 1
    QUESTION = 2
    WARNING = 3
    ERROR = 4


class MessageBoxButtonSet(IntEnum):
    """
    Standard sets of buttons to use in a message box.
    """

    OK = 1
    OKCANCEL = 2
    CLOSE = 3
    YESNO = 4
    YESNOCANCEL = 5
    RETRYCANCEL = 6


MESSAGE_BOX_ICON_PATHS = {
    MessageBoxIcon.INFO: "images/custom/dialog-information.png",
    MessageBoxIcon.QUESTION: "images/custom/dialog-question.png",
    MessageBoxIcon.WARNING: "images/custom/dialog-warning.png",
    MessageBoxIcon.ERROR: "images/custom/dialog-error.png"
}


class MessageBox(ButtonMixin, tk.Toplevel):
    """
    Message box modal dialog.

    Attributes
    ----------
    message : str
        The message text of the message box.
    icon : MessageBoxIcon
        The standard icon to display with the message.
    custom_icon : PhotoImage
        The custom icon to display with the message.
    button_set : MessageBoxButtonSet
        The set of buttons to display in the message box.
    button_list : list[ButtonName]
        A list of buttons to display in the message box, overrides button_set.
    default : int
        The default button number.
    internal_frame : ttk.Frame
        A frame to hold the message box contents.
    """

    def __init__(
        self, parent: tk.Misc | None = None, *,
        title: str | None = None,
        message: str | None = None,
        icon: MessageBoxIcon | None = None,
        custom_icon: tk.PhotoImage | None = None,
        button_set: MessageBoxButtonSet = MessageBoxButtonSet.OK,
        button_list: list[ButtonName] | None = None,
        default: int = -1
    ) -> None:
        """
        Construct a messagebox.

        Parameters
        ----------
        parent : Misc, optional
            The parent widget.
        title : str, optional
            The title to display in the window title bar.
        message : str, optional
            The message text of the messagebox.
        icon : MessageBoxIcon, optional
            The standard icon to display with the message.
        custom_icon : PhotoImage, optional
            The custom icon to display with the message.
        button_set : MessageBoxButtonSet
            The set of buttons to display in the message box.
        button_list : list[ButtonName]
            A list of buttons to display in the message box, overrides button_set.
        default : int
            The default button number.
        """
        super().__init__(parent, class_="MessageBox")
        self.message = message
        self.icon = icon
        self.custom_icon = custom_icon
        self.button_set = button_set
        self.button_list = button_list
        self.default = default
        self._set_standard_icon()
        self.internal_frame = ttk.Frame(self)
        self.internal_frame.grid(sticky=tk.NSEW)
        self.title(title)
        self.bind("<KeyPress-Escape>", self.dismiss)
        self.create_widgets()
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.transient(parent)  # type: ignore[arg-type]
        self.wm_withdraw()

    def show(self) -> ButtonName:
        """
        Show the constructed message box as a modal dialog.

        Returns
        -------
        ButtonName - the ButtonName of the button pressed.
        """
        self.wm_deiconify()
        self.wait_visibility()
        self.grab_set()
        self.wait_window()
        return self.result

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the message box.
        """
        message = self.message if self.message else ""
        label = ttk.Label(
            self.internal_frame, text=message, compound=tk.LEFT, wraplength=320
        )
        if self.custom_icon is not None:
            label.configure(image=self.custom_icon)
        label.grid(row=0, column=0, sticky=tk.NSEW, padx=INTERNAL_PAD, pady=INTERNAL_PAD)
        if self.button_list is not None:
            with suppress(KeyError):
                buttons = [self.button_definitions[button] for button in self.button_list]
                self.add_buttons(self.internal_frame, buttons=buttons, default=self.default)
        else:
            self.add_buttons_from_button_set()()

    def _set_standard_icon(self) -> None:
        if self.custom_icon is not None:
            return
        file: str | None = None
        if self.icon is not None:
            with suppress(KeyError):
                file = MESSAGE_BOX_ICON_PATHS[self.icon]
        if file is not None:
            self.custom_icon = tk.PhotoImage(file=get_full_path(file))

    def add_buttons_from_button_set(self) -> Callable:
        """
        Add buttons based on the button set.

        Returns
        -------
        Callable - a method which adds one or more buttons to the message box.
        """
        button_set_command = {
            MessageBoxButtonSet.OK: self.add_ok_button,
            MessageBoxButtonSet.OKCANCEL: self.add_ok_cancel_buttons,
            MessageBoxButtonSet.CLOSE: self.add_close_button,
            MessageBoxButtonSet.YESNO: self.add_yes_no_buttons,
            MessageBoxButtonSet.YESNOCANCEL: self.add_yes_no_cancel_buttons,
            MessageBoxButtonSet.RETRYCANCEL: self.add_retry_cancel_buttons
        }
        with suppress(KeyError):
            return button_set_command[self.button_set]
        return lambda: None

    def add_ok_button(self) -> None:
        """
        Add an OK button to the bottom row of the modal dialog.
        """
        buttons = [
            self.button_definitions[ButtonName.OK]
        ]
        self.add_buttons(self.internal_frame, buttons=buttons, default=0)

    def add_ok_cancel_buttons(self) -> None:
        """
        Add OK and Cancel buttons to the bottom row of the modal dialog.
        """
        buttons = [
            self.button_definitions[ButtonName.CANCEL],
            self.button_definitions[ButtonName.OK]
        ]
        self.add_buttons(self.internal_frame, buttons=buttons, default=1)

    def add_close_button(self) -> None:
        """
        Add a Close button to the bottom row of the modal dialog.
        """
        buttons = [
            self.button_definitions[ButtonName.CLOSE]
        ]
        self.add_buttons(self.internal_frame, buttons=buttons, default=0)

    def add_yes_no_buttons(self) -> None:
        """
        Add Yes and No buttons to the bottom row of the modal dialog.
        """
        buttons = [
            self.button_definitions[ButtonName.NO],
            self.button_definitions[ButtonName.YES]
        ]
        self.add_buttons(self.internal_frame, buttons=buttons, default=1)

    def add_yes_no_cancel_buttons(self) -> None:
        """
        Add OK and Cancel buttons to the bottom row of the modal dialog.
        """
        buttons = [
            self.button_definitions[ButtonName.CANCEL],
            self.button_definitions[ButtonName.NO],
            self.button_definitions[ButtonName.YES]
        ]
        self.add_buttons(self.internal_frame, buttons=buttons, default=2)

    def add_retry_cancel_buttons(self) -> None:
        """
        Add Retry and Cancel buttons to the bottom row of the modal dialog.
        """
        buttons = [
            self.button_definitions[ButtonName.CANCEL],
            self.button_definitions[ButtonName.RETRY]
        ]
        self.add_buttons(self.internal_frame, buttons=buttons, default=1)
