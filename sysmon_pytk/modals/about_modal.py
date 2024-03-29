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
from uuid import uuid4

from .._common import INTERNAL_PAD
from ..app_locale import get_translator
from ..file_utils import get_full_path, get_main_script
from ..translator import TRANSLATORS, Translator
from ..widgets import ScrollingText, TextToolTip
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
        text = ScrollingText(
            notebook, font=self.base_font, height=11, width=50, wrap=tk.WORD,
            undo=False, relief=tk.FLAT, spacing1=INTERNAL_PAD
        )
        tab = text.get_frame()
        text.image_create(tk.END, image=self.logo)
        text.insert(tk.END, "\n")
        text.insert(tk.END, self.about.get_name() + "\n", "large")
        text.insert(tk.END, _("Version {}").format(self.about.get_version_string()) + "\n")
        copyright_text = self.about.get_copyright_text()
        if copyright_text:
            text.insert(tk.END, copyright_text + "\n")
        if self.about.url:
            token = uuid4().hex
            text.insert(tk.END, _("Source Code"), ("link", token))
            text.insert(tk.END, self.about.url, "linkurl")
            text.insert(tk.END, "\n")
            TextToolTip(text, self.about.url, token)
        text.tag_add("center", "1.0", "end-1c")
        text.insert(tk.END, self.about.description)
        text.config(state=tk.DISABLED, padx=INTERNAL_PAD)
        return tab

    def create_translators_tab(self, notebook: ttk.Notebook) -> ttk.Frame:
        """
        Create the Translators page of the Notebook widget.
        """
        text = ScrollingText(
            notebook, font=self.base_font, height=10, width=50, wrap=tk.WORD,
            undo=False, relief=tk.FLAT
        )
        tab = text.get_frame()
        for language, translator_list in TRANSLATORS.items():
            text.insert(tk.END, f"{language}: ", "bold")
            for idx, translator in enumerate(translator_list):
                self._add_translator(text, translator, idx, len(translator_list))
        text.delete("end-1c")  # remove the final "\n"
        text.config(state=tk.DISABLED, spacing1=4, spacing2=4, spacing3=4)
        return tab

    def _add_translator(
        self, text: tk.Text, translator: Translator, idx: int, max_items: int
    ) -> None:
        text.insert(tk.END, translator.name)
        if translator.github_username:
            token = uuid4().hex
            text.insert(tk.END, " (")
            text.insert(tk.END, f"{translator.github_username} @ GitHub", ("link", token))
            text.insert(tk.END, translator.github_url(), "linkurl")
            text.insert(tk.END, ")")
            TextToolTip(text, translator.github_url(), token)
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
        text = ScrollingText(
            notebook, font=self.base_font, height=15, width=50, wrap=tk.WORD,
            undo=False, relief=tk.FLAT
        )
        tab = text.get_frame()
        if license_data.full_license:
            license_text = [
                paragraph.replace(
                    "\n", " "
                ) for paragraph in license_data.full_license.split("\n\n")
            ]
            text.insert(tk.END, "\n\n".join(license_text))
        elif license_data.license_name:
            text.config(spacing1=4, spacing2=4, spacing3=4, height=5)
            text.insert(tk.END, license_data.license_name + "\n")
            if license_data.license_url:
                token = uuid4().hex
                text.insert(tk.END, _("Full license text available here"), ("link", token))
                text.insert(tk.END, license_data.license_url, "linkurl")
                TextToolTip(text, license_data.license_url, token)
            text.tag_add("center", "1.0", "end-1c")
        text.config(state=tk.DISABLED)
        return tab
