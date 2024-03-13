# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Modal dialogs base class.
"""

from abc import abstractmethod
from typing import Optional, final
import tkinter as tk
from tkinter import ttk, Misc, font

from .. import font_utils


class ModalDialog(tk.Toplevel):
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
    """

    def __init__(
        self, parent: Optional[Misc] = None, title: Optional[str] = None,
        iconpath: Optional[str] = None, class_: str = "ModalDialog"
    ):
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
        self.title(title)
        self.iconpath = iconpath
        if iconpath is not None:
            self.iconphoto(False, tk.PhotoImage(file=iconpath))
        self.base_font = font.nametofont("TkDefaultFont")
        self.large_font = font_utils.modify_named_font(
            "TkDefaultFont", size=self.base_font.actual()["size"]+4
        )
        self.bold_font = font_utils.modify_named_font(
            "TkDefaultFont", weight="bold"
        )
        self.fixed_font = font.nametofont("TkFixedFont")
        self.init_styles()
        self.internal_frame = ttk.Frame(self)
        self.internal_frame.grid()
        self.create_widgets()
        self.update_screen()
        self.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.bind("<KeyPress-Escape>", self.dismiss)
        self.bind("<KeyPress-Return>", self.save_and_dismiss)
        self.bind("<KeyPress-KP_Enter>", self.save_and_dismiss)
        self.transient(parent)  # type: ignore
        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    @final
    def dismiss(self, *_args):
        """
        Dismiss the modal dialog.

        This should be bound to Cancel and Close buttons in subclasses.
        """
        self.grab_release()
        self.destroy()

    @final
    def save_and_dismiss(self, *_args):
        """
        Save what was entered in the modal dialog and dismiss it.

        This should be bound to OK and Save buttons in subclasses.
        """
        self.on_save()
        self.dismiss()

    @abstractmethod
    def on_save(self):
        """
        Save what was entered in the modal dialog.
        """

    @abstractmethod
    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.
        """

    @abstractmethod
    def create_widgets(self):
        """
        Create the widgets to be displayed in the modal dialog.
        """

    @abstractmethod
    def update_screen(self):
        """
        Update the modal dialog window.
        """
