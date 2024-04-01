# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Application settings modal dialog.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from .. import _common, desktop_menu
from ..app_locale import LANGUAGES, get_translator
from ..widgets import DropDown
from ._base_modal import ModalDialog
from .font_modal import FontChooser

if TYPE_CHECKING:
    from tkinter import Misc

    from ..settings import Settings

_ = get_translator()

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-instance-attributes

THEMES = {
    _("Light"): "Light",
    _("Dark"): "Dark",
    _("Same as System"): "Same as System"
}


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
    add_menu_icon : IntVar
        A flag to indicate whether the application should add a menu icon.
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
        self, settings: Settings, parent: Misc | None = None,
        title: str | None = None, iconpath: str | None = None
    ) -> None:
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
        self.always_on_top = tk.IntVar()
        self.always_on_top.set(self.settings.always_on_top)
        self.add_menu_icon = tk.IntVar()
        self.add_menu_icon.set(self.settings.add_menu_icon)
        self.fonts = {
            "regular": self.settings.regular_font.get_full_font().get_string(),
            "fixed": self.settings.fixed_font.get_full_font().get_string()
        }
        super().__init__(parent, title=title, iconpath=iconpath)

    def update_screen(self) -> None:
        """
        Update the modal dialog window.

        This dialog does not require screen updates.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        for row in range(1, 7):
            self.internal_frame.rowconfigure(row, weight=1)
        self.internal_frame.columnconfigure(2, weight=1)
        ttk.Label(
            self.internal_frame, text=_("Language"), font=self.base_font
        ).grid(row=1, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.langbox = DropDown(
            self.internal_frame, dictionary=LANGUAGES, state=["readonly"],
            exportselection=0, font=self.base_font
        )
        self.langbox.set(self.settings.language)
        self.langbox.grid(
            row=1, column=2, sticky=tk.EW, pady=_common.INTERNAL_PAD,
            padx=(0, _common.INTERNAL_PAD)
        )
        self.langbox.bind(
            "<<ComboboxSelected>>", lambda event: event.widget.selection_clear()
        )
        ttk.Label(
            self.internal_frame, text=_("Theme"), font=self.base_font
        ).grid(row=2, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        # Language translation is used as keys, and English is used as values
        # so that English is stored in the settings file, while allowing the
        # user to choose their theme based on their selected language.
        self.themebox = DropDown(
            self.internal_frame, dictionary=THEMES, state=["readonly"],
            exportselection=0, font=self.base_font
        )
        self.themebox.set(self.settings.theme)
        self.themebox.grid(
            row=2, column=2, sticky=tk.EW, pady=_common.INTERNAL_PAD,
            padx=(0, _common.INTERNAL_PAD)
        )
        self.themebox.bind(
            "<<ComboboxSelected>>", lambda event: event.widget.selection_clear()
        )
        ttk.Checkbutton(
            self.internal_frame, text=_("Always on top"), variable=self.always_on_top,
            style="Switch.TCheckbutton"
        ).grid(
            row=3, column=2, sticky=tk.EW, padx=_common.INTERNAL_PAD,
            pady=_common.INTERNAL_PAD
        )
        ttk.Label(
            self.internal_frame, text=_("Regular Font"), font=self.base_font
        ).grid(row=4, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.font_button = ttk.Button(
            self.internal_frame, text=self.fonts["regular"], command=self.show_font_chooser
        )
        self.font_button.grid(
            row=4, column=2, sticky=tk.EW, padx=_common.INTERNAL_PAD,
            pady=_common.INTERNAL_PAD
        )
        ttk.Label(
            self.internal_frame, text=_("Monospace Font"), font=self.base_font
        ).grid(row=5, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.fixed_font_button = ttk.Button(
            self.internal_frame, text=self.fonts["fixed"], command=self.show_fixedfont_chooser
        )
        self.fixed_font_button.grid(
            row=5, column=2, sticky=tk.EW, padx=_common.INTERNAL_PAD,
            pady=_common.INTERNAL_PAD
        )
        ttk.Checkbutton(
            self.internal_frame, text=_("Add to desktop menu system"),
            variable=self.add_menu_icon, style="Switch.TCheckbutton",
        ).grid(
            row=6, column=1, columnspan=2, sticky=tk.NS+tk.E, padx=_common.INTERNAL_PAD,
            pady=_common.INTERNAL_PAD
        )
        self.add_ok_cancel_buttons()
        self.add_sizegrip()

    def show_font_chooser(self, *_args) -> None:
        """
        Show a font chooser dialog.
        """
        chooser = FontChooser(
            self.parent, current_font=self.settings.regular_font.get_full_font(),
            iconpath=self.iconpath
        )
        chosen_font = chooser.get_font()
        if chosen_font:
            self.settings.regular_font.set_full_font(chosen_font)
            self.font_button.config(
                text=self.settings.regular_font.get_full_font().get_string()
            )
        else:
            self.font_button.config(
                text=_("Select a font")
            )

    def show_fixedfont_chooser(self, *_args) -> None:
        """
        Show a font chooser dialog.
        """
        chooser = FontChooser(
            self.parent, current_font=self.settings.fixed_font.get_full_font(),
            iconpath=self.iconpath
        )
        chosen_font = chooser.get_font()
        if chosen_font:
            self.settings.fixed_font.set_full_font(chosen_font)
            self.fixed_font_button.config(
                text=self.settings.fixed_font.get_full_font().get_string()
            )
        else:
            self.font_button.config(
                text=_("Select a font")
            )

    def on_save(self, *_args) -> None:
        """
        Save the entered settings.
        """
        old_language = self.settings.language
        self.update_settings()
        self.generate_change_events(old_language)

    def update_settings(self) -> None:
        """
        Update the app settings.
        """
        self.settings.language = self.langbox.get()
        self.settings.theme = self.themebox.get()
        self.settings.always_on_top = self.always_on_top.get()
        if self.add_menu_icon.get():
            result = desktop_menu.install_desktop_file(self)
            self.settings.add_menu_icon = 1 if result else 0
        else:
            desktop_menu.uninstall_desktop_file()
            self.settings.add_menu_icon = 0
        self.settings.write_settings()

    def generate_change_events(self, old_language: str) -> None:
        """
        Generate change events based on the new settings.
        """
        if old_language != self.langbox.get():
            self.save_dismiss_event("<<LanguageChanged>>")
        new_regular_font = self.settings.regular_font.get_full_font().get_string()
        new_fixed_font = self.settings.fixed_font.get_full_font().get_string()
        if self.fonts["regular"] != new_regular_font:
            self.save_dismiss_event("<<FontChanged>>")
        if self.fonts["fixed"] != new_fixed_font:
            self.save_dismiss_event("<<FontChanged>>")
        self.save_dismiss_event("<<SettingsChanged>>")
