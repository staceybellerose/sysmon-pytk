# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Themed message boxes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .messagebox_base import MessageBox, MessageBoxButtonSet, MessageBoxIcon

if TYPE_CHECKING:
    from tkinter import Misc

    from ..widgets.button_mixin import ButtonName


def show_message(parent: Misc | None, title: str, message: str) -> ButtonName:
    """
    Display a message box to show a message.
    """
    return MessageBox(
        parent, title=title, message=message, icon=MessageBoxIcon.QUESTION,
        button_set=MessageBoxButtonSet.OK
    ).show()


def show_warning(parent: Misc | None, title: str, message: str) -> ButtonName:
    """
    Display a message box to show a warning.
    """
    return MessageBox(
        parent, title=title, message=message, icon=MessageBoxIcon.WARNING,
        button_set=MessageBoxButtonSet.OK
    ).show()


def show_error(parent: Misc | None, title: str, message: str) -> ButtonName:
    """
    Display a message box to show an error.
    """
    return MessageBox(
        parent, title=title, message=message, icon=MessageBoxIcon.ERROR,
        button_set=MessageBoxButtonSet.OK
    ).show()


def ask_ok_cancel(parent: Misc | None, title: str, message: str) -> ButtonName:
    """
    Display a message box to ask a question with OK/Cancel buttons.
    """
    return MessageBox(
        parent, title=title, message=message, icon=MessageBoxIcon.QUESTION,
        button_set=MessageBoxButtonSet.OKCANCEL
    ).show()


def ask_yes_no(parent: Misc | None, title: str, message: str) -> ButtonName:
    """
    Display a message box to ask a question with Yes/No buttons.
    """
    return MessageBox(
        parent, title=title, message=message, icon=MessageBoxIcon.QUESTION,
        button_set=MessageBoxButtonSet.YESNO
    ).show()


def ask_yes_no_cancel(parent: Misc | None, title: str, message: str) -> ButtonName:
    """
    Display a message box to ask a question with Yes/No/Cancel buttons.
    """
    return MessageBox(
        parent, title=title, message=message, icon=MessageBoxIcon.QUESTION,
        button_set=MessageBoxButtonSet.YESNOCANCEL
    ).show()


def ask_retry_cancel(parent: Misc | None, title: str, message: str) -> ButtonName:
    """
    Display a message box to ask a question with Retry/Cancel buttons.
    """
    return MessageBox(
        parent, title=title, message=message, icon=MessageBoxIcon.QUESTION,
        button_set=MessageBoxButtonSet.RETRYCANCEL
    ).show()
