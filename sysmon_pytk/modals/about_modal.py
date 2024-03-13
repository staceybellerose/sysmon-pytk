# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Display metadata about the application in a modal dialog.
"""

import dataclasses
from typing import Optional
import tkinter as tk
from tkinter import ttk

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
        if self.copyright_year != "":
            return f"© {self.copyright_year} {self.author}"
        return f"© {self.author}"


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
        self.internal_frame.configure(padding=INTERNAL_PAD)
        notebook = ttk.Notebook(self.internal_frame)
        notebook.grid(sticky=tk.W+tk.E+tk.N, pady=INTERNAL_PAD)
        tab1 = ttk.Frame(notebook)
        row = 0
        ttk.Label(tab1, image=self.logo).grid(row=row)
        row += 1
        if self.about.app_name != "":
            ttk.Label(
                tab1, text=self.about.app_name, font=self.large_font
            ).grid(row=row)
            row += 1
        if self.about.version != "":
            version = _("Version {}").format(self.about.version)
            ttk.Label(
                tab1, text=version, font=self.base_font
            ).grid(row=row)
            row += 1
        if self.about.author != "":
            ttk.Label(
                tab1, text=self.about.get_copyright_text(), font=self.base_font
            ).grid(row=row)
            row += 1
        if self.about.url != "":
            link1style = UrlLabel.test_web_protocol(
                self.about.url, "About_URL.System.TLabel", "System.TLabel"
            )
            UrlLabel(
                tab1, text=_("Source Code"), url=self.about.url,
                style=link1style, font=self.base_font, show_tooltip=True
            ).grid(row=row)
            row += 1
        if self.about.description != "":
            ttk.Label(
                tab1, text=self.about.description, wraplength=450, font=self.base_font
            ).grid(row=row)
            row += 1
        notebook.add(tab1, text=self.title(), sticky=tk.N, padding=INTERNAL_PAD)
        tab2 = self.create_translators_tab(notebook)
        notebook.add(tab2, text=_("Translators"), sticky=tk.N, padding=INTERNAL_PAD)
        if self.about.license is not None:
            tab3 = self.create_license_tab(notebook, self.about.license)
            notebook.add(tab3, text=_("License"), sticky=tk.N)
        notebook.enable_traversal()
        ttk.Button(
            self.internal_frame, text=_("Close"), command=self.dismiss, style='Accent.TButton'
        ).grid(sticky=tk.E)

    def create_translators_tab(
        self, notebook: ttk.Notebook
    ) -> ttk.Frame:
        """
        Create the Translators page of the Notebook widget.
        """
        tab = ttk.Frame(notebook)
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
        text.grid(row=0, column=0)
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
            text.grid(row=0, column=0)
            text_scroller = ttk.Scrollbar(tab, orient=tk.VERTICAL)
            text_scroller.grid(row=0, column=1, sticky=tk.N+tk.S)
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
