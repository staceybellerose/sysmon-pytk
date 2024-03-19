# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Display metadata about the application in a modal dialog.
"""

import dataclasses
import tkinter as tk
from tkinter import BaseWidget, ttk
from tkinter.font import Font
from typing import Optional

from .._common import INTERNAL_PAD
from ..app_locale import get_translator
from ..file_utils import get_full_path
from ..translator import TRANSLATORS, Translator
from ..widgets import UrlLabel
from ._base_modal import ModalDialog

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
    license: Optional[LicenseMetadata] = None

    def get_copyright_text(self) -> str:
        """
        Build the copyright text based on year and author.
        """
        if self.author != "":
            if self.copyright_year != "":
                return f"© {self.copyright_year} {self.author}"
            return f"© {self.author}"
        return ""


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

    def __init__(self, parent, about: AboutMetadata, iconpath=None):
        self.about = about
        title = _("About {}").format(about.app_name).strip()
        self.logo = tk.PhotoImage(file=get_full_path("images/icon-lg.png"))
        self._about_description: Optional[tk.Text] = None
        super().__init__(parent, title=title, iconpath=iconpath, class_="AboutBox")

    def update_screen(self):
        """
        Update the modal dialog window.

        This dialog does not require screen updates.
        """

    def on_save(self):
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def create_widgets(self):
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
        row = 0
        ttk.Label(tab, image=self.logo).grid(row=row)
        row += 1
        row = self._add_label_if_string(
            tab, self.about.app_name, self.large_font, row
        )
        row = self._add_label_if_string(
            tab, _("Version {}").format(self.about.version), self.base_font, row
        )
        row = self._add_label_if_string(
            tab, self.about.get_copyright_text(), self.base_font, row
        )
        if self.about.url != "":
            link1style = UrlLabel.test_web_protocol(
                self.about.url, "URL.TLabel", "System.TLabel"
            )
            UrlLabel(
                tab, text=_("Source Code"), url=self.about.url,
                style=link1style, font=self.base_font, show_tooltip=True,
                anchor=tk.CENTER
            ).grid(row=row, sticky=tk.NSEW, pady=(0, INTERNAL_PAD))
            tab.rowconfigure(row, weight=1)
            row += 1
        if self.about.description != "":
            self._about_description = tk.Text(
                tab, font=self.base_font, height=5, width=50, wrap=tk.WORD,
                undo=False, relief=tk.FLAT
            )
            self._about_description.insert(tk.END, self.about.description)
            self._about_description.config(state=tk.DISABLED)
            self._about_description.grid(
                row=row, sticky=tk.NSEW, padx=(INTERNAL_PAD, 0)
            )
            tab.rowconfigure(row, weight=1)
            row += 1
        return tab

    def create_translators_tab(self, notebook: ttk.Notebook) -> ttk.Frame:
        """
        Create the Translators page of the Notebook widget.
        """
        tab = ttk.Frame(notebook)
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)
        text = tk.Text(
            tab, font=self.base_font, height=4, width=50, wrap=tk.WORD,
            undo=False, relief=tk.FLAT
        )
        for language, translator_list in TRANSLATORS.items():
            self._add_translators(text, language, translator_list)
        text.tag_configure("language", font=self.bold_font)
        text.config(state=tk.DISABLED, spacing1=4, spacing2=4, spacing3=4)
        text.grid(row=0, column=0, sticky=tk.NSEW)
        # FOR LATER IF SCROLLING IS NEEDED
        # text_scroller = ttk.Scrollbar(tab, orient=tk.VERTICAL)
        # text_scroller.grid(row=0, column=1, sticky=tk.N+tk.S)
        # text.config(yscrollcommand=text_scroller.set)
        # text_scroller.config(command=text.yview)
        return tab

    def _add_translators(
        self, text: tk.Text, language: str, translator_list: list[Translator]
    ):
        text.insert(tk.END, f"{language}: ", ("language",))
        for idx, translator in enumerate(translator_list):
            text.insert(tk.END, translator.name)
            if translator.github_username != "":
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
            if idx < len(translator_list)-1:
                text.insert(tk.END, ",")
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
        if license_data.full_license != "":
            license_text = [
                line.replace(
                    "\n", " "
                ) for line in license_data.full_license.split("\n\n")
            ]
            text = tk.Text(
                tab, font=self.base_font, height=16, width=50, wrap=tk.WORD,
                undo=False, relief=tk.FLAT
            )
            text.insert(tk.END, "\n\n".join(license_text))
            text.config(state=tk.DISABLED)
            text.grid(row=0, column=0, sticky=tk.NSEW)
            text_scroller = ttk.Scrollbar(tab, orient=tk.VERTICAL)
            text_scroller.grid(row=0, column=1, sticky=tk.NSEW)
            text.config(yscrollcommand=text_scroller.set)
            text_scroller.config(command=text.yview)
        elif license_data.license_name != "":
            tk.Label(
                tab, font=self.base_font, text=license_data.license_name
            ).grid(row=0, pady=INTERNAL_PAD)
            if license_data.license_url != "":
                link2style = UrlLabel.test_web_protocol(
                    license_data.license_url, "URL.TLabel", "System.TLabel"
                )
                UrlLabel(
                    tab, text=_("Full license text available here"),
                    url=license_data.license_url, style=link2style,
                    show_tooltip=True
                ).grid(row=1, pady=INTERNAL_PAD)
        return tab

    def _add_label_if_string(
        self, parent: BaseWidget, text: str, font: Font, row: int
    ) -> int:
        if text != "":
            ttk.Label(
                parent, text=text, font=font, anchor=tk.CENTER
            ).grid(row=row, sticky=tk.NSEW, pady=(0, INTERNAL_PAD))
            parent.rowconfigure(row, weight=1)
            row += 1
        return row
