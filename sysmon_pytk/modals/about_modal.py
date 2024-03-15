# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Display metadata about the application in a modal dialog.
"""

import dataclasses
from typing import Optional
import tkinter as tk
from tkinter import ttk, BaseWidget
from tkinter.font import Font

from ..widgets import UrlLabel
from .._common import is_dark, INTERNAL_PAD
from ..file_utils import get_full_path
from ..translator import TRANSLATORS
from ..app_locale import get_translator

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
        super().__init__(parent, title=title, iconpath=iconpath, class_="AboutBox")

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.
        """
        style = ttk.Style()
        background = style.lookup("TLabel", "background")
        dark_mode = is_dark(f"{background}")
        style.configure("System.TLabel", font="TkDefaultFont")
        style.configure(
            "About_URL.System.TLabel",
            foreground="#66CCFF" if dark_mode else "#0000EE"
        )

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
        self.internal_frame.configure(padding=INTERNAL_PAD/2)
        self.internal_frame.rowconfigure(0, weight=1)
        self.internal_frame.columnconfigure(0, weight=1)
        notebook = ttk.Notebook(self.internal_frame)
        notebook.grid(row=0, sticky=tk.NSEW, pady=INTERNAL_PAD/2)
        tab1 = ttk.Frame(notebook)
        tab1.rowconfigure(0, weight=1)
        tab1.columnconfigure(0, weight=1)
        row = 0
        ttk.Label(tab1, image=self.logo).grid(row=row)
        row += 1
        row = self._add_label_if_string(
            tab1, self.about.app_name, self.large_font, row
        )
        row = self._add_label_if_string(
            tab1, _("Version {}").format(self.about.version), self.base_font, row
        )
        row = self._add_label_if_string(
            tab1, self.about.get_copyright_text(), self.base_font, row
        )
        if self.about.url != "":
            link1style = UrlLabel.test_web_protocol(
                self.about.url, "About_URL.System.TLabel", "System.TLabel"
            )
            UrlLabel(
                tab1, text=_("Source Code"), url=self.about.url,
                style=link1style, font=self.base_font, show_tooltip=True,
                anchor=tk.CENTER
            ).grid(row=row, sticky=tk.NSEW, pady=(0, INTERNAL_PAD))
            tab1.rowconfigure(row, weight=1)
            row += 1
        if self.about.description != "":
            text = tk.Text(
                tab1, font=self.base_font, height=5, width=50, wrap=tk.WORD,
                undo=False, relief=tk.FLAT
            )
            text.insert(tk.END, self.about.description)
            text.config(state=tk.DISABLED)
            text.grid(row=row, sticky=tk.NSEW)
            tab1.rowconfigure(row, weight=1)
            row += 1
        notebook.add(tab1, text=self.title(), sticky=tk.NSEW, padding=INTERNAL_PAD)
        tab2 = self.create_translators_tab(notebook)
        notebook.add(tab2, text=_("Translators"), sticky=tk.NSEW, padding=INTERNAL_PAD)
        if self.about.license is not None:
            tab3 = self.create_license_tab(notebook, self.about.license)
            notebook.add(tab3, text=_("License"), sticky=tk.NSEW)
        notebook.enable_traversal()
        ttk.Button(
            self.internal_frame, text=_("Close"), command=self.dismiss, style='Accent.TButton'
        ).grid(row=1, sticky=tk.E, pady=INTERNAL_PAD/2)
        ttk.Sizegrip(self.internal_frame).grid(row=2, column=0, sticky=tk.SE)

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
            text.insert(tk.END, f"{language}: ", ('language',))
            for idx, translator in enumerate(translator_list):
                text.insert(tk.END, translator.name)
                if translator.github_username != "":
                    linkstyle = UrlLabel.test_web_protocol(
                        self.about.url, "About_URL.System.TLabel", "System.TLabel"
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
        text.tag_configure('language', font=self.bold_font)
        text.config(state=tk.DISABLED, spacing1=4, spacing2=4, spacing3=4)
        text.grid(row=0, column=0, sticky=tk.NSEW)
        # FOR LATER IF SCROLLING IS NEEDED
        # text_scroller = ttk.Scrollbar(tab, orient=tk.VERTICAL)
        # text_scroller.grid(row=0, column=1, sticky=tk.N+tk.S)
        # text.config(yscrollcommand=text_scroller.set)
        # text_scroller.config(command=text.yview)
        return tab

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
                    license_data.license_url,
                    "About_URL.System.TLabel", "System.TLabel"
                )
                UrlLabel(
                    tab, text=_("Full license text available here"),
                    url=license_data.license_url, style=link2style,
                    show_tooltip=True
                ).grid(row=1, pady=INTERNAL_PAD)
        return tab
