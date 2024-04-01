# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Mixin class for standard button sets in dialogs.
"""

from __future__ import annotations

import dataclasses
import tkinter as tk
from enum import IntEnum
from tkinter import ttk
from typing import Any, Callable, TypeVar, Union

from .._common import INTERNAL_PAD
from ..app_locale import get_translator

_ = get_translator()

WidgetFrame = TypeVar("WidgetFrame", bound=Union[ttk.Frame, tk.Frame])


class ButtonName(IntEnum):
    """
    Standard button names.
    """

    NONE = 0
    OK = 1
    CANCEL = 2
    CLOSE = 3
    YES = 4
    NO = 5
    RETRY = 6


@dataclasses.dataclass
class ButtonDefinition:
    """
    Necessary metadata for creating a button.
    """

    text: str
    command: Callable[[], Any]


class ButtonMixin:  # pylint: disable=too-few-public-methods
    """
    Mixin class for standard button sets in dialogs.

    Attributes
    ----------
    result : ButtonName
        The button pressed to close the message box.
    button_definitions : dict[ButtonName, ButtonDefinition]
        A dictionary of standard buttons available to use.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.result = ButtonName.NONE
        self.init_standard_buttons()
        self.toplevel: tk.Tk | tk.Toplevel | None = None

    def add_buttons(
        self, frame: WidgetFrame, *, buttons: list[ButtonDefinition],
        default: int = -1
    ) -> None:
        """
        Add buttons to the provided frame at the bottom, justified right.

        Parameters
        ----------
        frame : WidgetFrame (tk.Frame or ttk.Frame)
            The frame to which the buttons will be added
        buttons : list[ButtonDefinition]
            The list of buttons to add
        default : int
            The default button, displayed with style="Accent.TButton"
        """
        self.toplevel = frame.winfo_toplevel()
        max_columns, max_rows = frame.grid_size()
        buttonframe = ttk.Frame(frame)
        buttonframe.grid(
            row=max_rows, column=0, sticky=tk.E, columnspan=max_columns,
            pady=(0, INTERNAL_PAD)
        )
        for num, button in enumerate(buttons):
            btn = ttk.Button(buttonframe, text=button.text, command=button.command)
            if num == default:
                btn.configure(style="Accent.TButton")
                self.toplevel.bind(
                    "<KeyPress-Return>", button.command  # type: ignore[arg-type]
                )
                self.toplevel.bind(
                    "<KeyPress-KP_Enter>", button.command  # type: ignore[arg-type]
                )
            btn.grid(row=0, column=num, padx=INTERNAL_PAD/2)

    def init_standard_buttons(self) -> None:
        """
        Define the button definitions.
        """
        self.button_definitions = {
            ButtonName.OK: ButtonDefinition(
                text=_("OK"), command=lambda: self._set_result(ButtonName.OK)
            ),
            ButtonName.CANCEL: ButtonDefinition(
                text=_("Cancel"), command=lambda: self._set_result(ButtonName.CANCEL)
            ),
            ButtonName.CLOSE: ButtonDefinition(
                text=_("Close"), command=lambda: self._set_result(ButtonName.CLOSE)
            ),
            ButtonName.YES: ButtonDefinition(
                text=_("Yes"), command=lambda: self._set_result(ButtonName.YES)
            ),
            ButtonName.NO: ButtonDefinition(
                text=_("No"), command=lambda: self._set_result(ButtonName.NO)
            ),
            ButtonName.RETRY: ButtonDefinition(
                text=_("Retry"), command=lambda: self._set_result(ButtonName.RETRY)
            ),
        }

    def _set_result(self, value: ButtonName) -> None:
        """
        Set the result to the ButtonName pressed.

        Parameters
        ----------
        value : ButtonName
            The ButtonName of the button pressed.
        """
        self.result = value
        self.dismiss()

    def dismiss(self, *_args) -> None:
        """
        Dismiss the window.
        """
        if self.toplevel is not None:
            self.toplevel.grab_release()
            self.toplevel.destroy()
