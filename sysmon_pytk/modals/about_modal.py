# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Display metadata about the application in a modal dialog.
"""

from __future__ import annotations

import dataclasses
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from .._common import INTERNAL_PAD
from ..app_locale import get_translator
from ..file_utils import get_full_path, get_main_script
from ..translator import TRANSLATORS, Translator
from ..widgets import AutoScrollbar, UrlLabel
from ._base_modal import ModalDialog

if TYPE_CHECKING:
    from tkinter import Misc

_ = get_translator()


@dataclasses.dataclass
class LicenseMetadata:
    """
    Metadata about the license used by the application.
    """

    full_license: str
    license_name: str
    license_url: str


@dataclasses.dataclass
class AboutMetadata:
    """
    Metadata about the application.
    """

    app_name: str
    version: str
    author: str
    copyright_year: str
    description: str
    url: str
    license: LicenseMetadata | None = None

    def get_copyright_text(self) -> str:
        """
        Build the copyright text based on year and author.
        """
        if self.author:
            if self.copyright_year:
                return f"© {self.copyright_year} {self.author}"
            return f"© {self.author}"
        return ""

    def get_name(self) -> str:
        """
        Return the app name meta data if available; otherwise, main script name.
        """
        return self.app_name if self.app_name else get_main_script()

    def get_version_string(self) -> str:
        """
        Return a string containing the version if available; otherwise, 0.0.1.
        """
        return self.version if self.version else "0.0.1"


class AboutDialog(ModalDialog):
    """
    Display metadata about the application in a modal dialog.

    Attributes
    ----------
    about : AboutMetadata
        Metadata about the application to be displayed.
    logo : PhotoImage
        A logo to be displayed.
    """

    def __init__(
        self, parent: Misc | None, about: AboutMetadata, iconpath: str | None = None
    ) -> None:
        self.about = about
        title = _("About {}").format(about.app_name).strip()
        self.logo = tk.PhotoImage(file=get_full_path("images/icon-lg.png"))
        super().__init__(parent, title=title, iconpath=iconpath, class_="AboutBox")

    def update_screen(self) -> None:
        """
        Update the modal dialog window.

        This dialog does not require screen updates.
        """

    def on_save(self) -> None:
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self.internal_frame.rowconfigure(0, weight=1)
        self.internal_frame.columnconfigure(0, weight=1)
        notebook = ttk.Notebook(self.internal_frame)
        notebook.grid(
            row=0, sticky=tk.NSEW, padx=INTERNAL_PAD/2, pady=INTERNAL_PAD/2
        )
        notebook.add(
            self.create_about_tab(notebook), text=self.title(), sticky=tk.NSEW
        )
        notebook.add(
            self.create_translators_tab(notebook), text=_("Translators"),
            sticky=tk.NSEW
        )
        if self.about.license is not None:
            notebook.add(
                self.create_license_tab(notebook, self.about.license),
                text=_("License"), sticky=tk.NSEW
            )
        notebook.enable_traversal()
        self.add_close_button()
        self.add_sizegrip()

    def create_about_tab(self, notebook: ttk.Notebook) -> ttk.Frame:
        """
        Create the About page of the Notebook widget.
        """
        tab = ttk.Frame(notebook)
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        text = tk.Text(
            tab, font=self.base_font, height=11, width=50, wrap=tk.WORD,
            undo=False, relief=tk.FLAT, spacing1=INTERNAL_PAD
        )
        text.tag_configure("center", justify="center")
        text.tag_configure("large", font=self.large_font)
        text.image_create(tk.END, image=self.logo)
        text.insert(tk.END, "\n")
        text.insert(tk.END, self.about.get_name() + "\n", "large")
        text.insert(tk.END, _("Version {}").format(self.about.get_version_string()) + "\n")
        copyright_text = self.about.get_copyright_text()
        if copyright_text:
            text.insert(tk.END, copyright_text + "\n")
        if self.about.url:
            link1style = UrlLabel.test_web_protocol(
                self.about.url, "URL.TLabel", "System.TLabel"
            )
            link = UrlLabel(
                tab, text=_("Source Code"), url=self.about.url,
                style=link1style, font=self.base_font, show_tooltip=True,
                anchor=tk.CENTER
            )
            text.window_create(tk.END, window=link)
            text.insert(tk.END, "\n")
        text.tag_add("center", "1.0", "end-1c")
        text.insert(tk.END, self.about.description)
        text.config(state=tk.DISABLED)
        text.grid(row=0, column=0, sticky=tk.NSEW, padx=(INTERNAL_PAD, 0))
        AutoScrollbar.add_to_widget(text, orient=tk.VERTICAL).grid(
            row=0, column=1, sticky=tk.NS
        )
        return tab

    def create_translators_tab(self, notebook: ttk.Notebook) -> ttk.Frame:
        """
        Create the Translators page of the Notebook widget.
        """
        tab = ttk.Frame(notebook)
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        text = tk.Text(
            tab, font=self.base_font, height=10, width=50, wrap=tk.WORD,
            undo=False, relief=tk.FLAT
        )
        for language, translator_list in TRANSLATORS.items():
            text.insert(tk.END, f"{language}: ", "language")
            for idx, translator in enumerate(translator_list):
                self._add_translator(text, translator, idx, len(translator_list))
        text.delete("end-1c")  # remove the final "\n"
        text.tag_configure("language", font=self.bold_font)
        text.config(state=tk.DISABLED, spacing1=4, spacing2=4, spacing3=4)
        text.grid(row=0, column=0, sticky=tk.NSEW)
        AutoScrollbar.add_to_widget(text, orient=tk.VERTICAL).grid(
            row=0, column=1, sticky=tk.NS
        )
        return tab

    def _add_translator(
        self, text: tk.Text, translator: Translator, idx: int, max_items: int
    ) -> None:
        text.insert(tk.END, translator.name)
        if translator.github_username:
            linkstyle = UrlLabel.test_web_protocol(
                self.about.url, "URL.TLabel", "System.TLabel"
            )
            link = UrlLabel(
                text,
                text=f"{translator.github_username} @ GitHub",
                url=translator.github_url(), style=linkstyle,
                font=self.base_font, show_tooltip=True
            )
            text.insert(tk.END, " (")
            text.window_create(tk.END, window=link)
            text.insert(tk.END, ")")
        if idx < max_items-1:
            text.insert(tk.END, ", ")
        else:
            text.insert(tk.END, "\n")

    def create_license_tab(
        self, notebook: ttk.Notebook, license_data: LicenseMetadata
    ) -> ttk.Frame:
        """
        Create the License details page of the Notebook widget.
        """
        tab = ttk.Frame(notebook)
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        if license_data.full_license:
            license_text = [
                line.replace(
                    "\n", " "
                ) for line in license_data.full_license.split("\n\n")
            ]
            text = tk.Text(
                tab, font=self.base_font, height=15, width=50, wrap=tk.WORD,
                undo=False, relief=tk.FLAT
            )
            text.insert(tk.END, "\n\n".join(license_text))
            text.config(state=tk.DISABLED)
            text.grid(row=0, column=0, sticky=tk.NSEW)
            AutoScrollbar.add_to_widget(text, orient=tk.VERTICAL).grid(
                row=0, column=1, sticky=tk.NS
            )
        elif license_data.license_name:
            tk.Label(
                tab, font=self.base_font, text=license_data.license_name
            ).grid(row=0, pady=INTERNAL_PAD)
            if license_data.license_url:
                link2style = UrlLabel.test_web_protocol(
                    license_data.license_url, "URL.TLabel", "System.TLabel"
                )
                UrlLabel(
                    tab, text=_("Full license text available here"),
                    url=license_data.license_url, style=link2style,
                    show_tooltip=True
                ).grid(row=1, pady=INTERNAL_PAD)
        return tab
