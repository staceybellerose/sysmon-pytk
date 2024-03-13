# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Application settings modal dialog.
"""

from typing import Optional
import tkinter as tk
from tkinter import ttk, Misc

import _common
from settings import Settings
from widgets import DropDown
from app_locale import _, LANGUAGES

from ._base_modal import ModalDialog
from .font_modal import FontChooser


class SettingsDialog(ModalDialog):
    """
    Manage application settings in a modal dialog.

    Attributes
    ----------
    settings : Settings
        The application settings to manage.
    always_on_top : IntVar
        A flag to indicate whether the application should always float on top
        of other windows.
    fonts : dict[str, str]
        A dictionary containing the currently-selected fonts, regular and monospace.
    langbox : DropDown
        A dropdown widget to manage the user's choice of language.
    themebox : DropDown
        A dropdown widget to manage the user's choice of theme.
    font_button : Button
        A button to open a `FontChooser` to manage the regular application font.
    fixed_font_button : Button
        A button to open a `FontChooser` to manage the monospace application font.
    """

    def __init__(
        self, settings: Settings, parent: Optional[Misc] = None,
        title: Optional[str] = None, iconpath: Optional[str] = None
    ):
        """
        Construct a Settings dialog.

        Parameters
        ----------
        settings : Settings
            The application settings to manage.
        parent : Misc, optional
            The parent widget.
        title : str, optional
            The title to display in the window title bar.
        iconpath : str, optional
            The path to the icon to display in the window title bar.
        """
        self.settings = settings
        super().__init__(parent, title=title, iconpath=iconpath)

    def update_screen(self):
        """
        Update the modal dialog window.

        This dialog does not require screen updates.
        """

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.
        """
        style = ttk.Style()
        style.configure("Switch.TCheckbutton", font=self.base_font)

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self.always_on_top = tk.IntVar()
        self.always_on_top.set(self.settings.get_always_on_top())
        self.fonts = {
            "regular": self.settings.regular_font.get_full_font().get_string(),
            "fixed": self.settings.fixed_font.get_full_font().get_string()
        }
        self.internal_frame.configure(padding=_common.INTERNAL_PAD)
        self.option_add('*TCombobox*Listbox.font', self.base_font)
        ttk.Label(
            self.internal_frame, text=_("Language"), font=self.base_font
        ).grid(row=1, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.langbox = DropDown(
            self.internal_frame, dictionary=LANGUAGES, state=["readonly"], exportselection=0,
            font=self.base_font
        )
        self.langbox.set(self.settings.get_language())
        self.langbox.grid(row=1, column=2, pady=_common.INTERNAL_PAD)
        self.langbox.bind("<<ComboboxSelected>>", self.change_combobox)
        ttk.Label(
            self.internal_frame, text=_("Theme"), font=self.base_font
        ).grid(row=2, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        # Language translation is used as keys, and English is used as values
        # so that English is stored in the settings file, while allowing the
        # user to choose their theme based on their selected language.
        themes = {
            _("Light"): "Light",
            _("Dark"): "Dark",
            _("Same as System"): "Same as System"
        }
        self.themebox = DropDown(
            self.internal_frame, dictionary=themes, state=["readonly"], exportselection=0,
            font=self.base_font
        )
        self.themebox.set(self.settings.get_theme())
        self.themebox.grid(row=2, column=2, pady=_common.INTERNAL_PAD)
        self.themebox.bind("<<ComboboxSelected>>", self.change_combobox)
        ttk.Checkbutton(
            self.internal_frame, text=_("Always on top"), variable=self.always_on_top,
            style='Switch.TCheckbutton'
        ).grid(
            row=3, column=2,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        ttk.Label(
            self.internal_frame, text=_("Regular Font"), font=self.base_font
        ).grid(row=4, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.font_button = ttk.Button(
            self.internal_frame, text=self.fonts["regular"], command=self.show_font_chooser
        )
        self.font_button.grid(
            row=4, column=2,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        ttk.Label(
            self.internal_frame, text=_("Monospace Font"), font=self.base_font
        ).grid(row=5, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.fixed_font_button = ttk.Button(
            self.internal_frame, text=self.fonts["fixed"], command=self.show_fixedfont_chooser
        )
        self.fixed_font_button.grid(
            row=5, column=2,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        buttonframe = ttk.Frame(self.internal_frame)
        ttk.Button(
            buttonframe, text=_("Cancel"), command=self.dismiss
        ).grid(row=1, column=1, padx=_common.INTERNAL_PAD/2)
        ttk.Button(
            buttonframe, text=_("OK"), command=self.save_and_dismiss,
            style='Accent.TButton'
        ).grid(row=1, column=2, padx=_common.INTERNAL_PAD/2)
        buttonframe.grid(row=6, column=1, columnspan=3, sticky=tk.E)

    def change_combobox(self, event: tk.Event):
        """
        Clear the selection when an item is selected in the combobox.
        """
        event.widget.selection_clear()

    def show_font_chooser(self, *_args):
        """
        Show a font chooser dialog.
        """
        chooser = FontChooser(
            self.parent, self.settings.regular_font.get_full_font(), self.iconpath
        )
        chosen_font = chooser.get_font()
        self.settings.regular_font.set_full_font(chosen_font)
        self.font_button.config(
            text=self.settings.regular_font.get_full_font().get_string()
        )

    def show_fixedfont_chooser(self, *_args):
        """
        Show a font chooser dialog.
        """
        chooser = FontChooser(
            self.parent, self.settings.fixed_font.get_full_font(), self.iconpath
        )
        chosen_font = chooser.get_font()
        self.settings.fixed_font.set_full_font(chosen_font)
        self.fixed_font_button.config(
            text=self.settings.fixed_font.get_full_font().get_string()
        )

    def on_save(self, *_args):
        """
        Save the entered settings.
        """
        old_language = self.settings.get_language()
        self.settings.set_language(self.langbox.get())
        self.settings.set_theme(self.themebox.get())
        self.settings.set_always_on_top(self.always_on_top.get())
        self.settings.write_settings()
        if old_language != self.langbox.get():
            self.parent.event_generate("<<LanguageChanged>>")
        if self.fonts["regular"] != self.settings.regular_font.get_full_font(
        ).get_string():
            self.parent.event_generate("<<FontChanged>>")
        if self.fonts["fixed"] != self.settings.fixed_font.get_full_font(
        ).get_string():
            self.parent.event_generate("<<FontChanged>>")
        self.parent.event_generate("<<SettingsChanged>>")
