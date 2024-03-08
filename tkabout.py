# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Display metadata about the application in a modal dialog.
"""

import dataclasses
from typing import Optional
import tkinter as tk
from tkinter import ttk, font

from tkmodal import ModalDialog
from widgets import UrlLabel
from _common import is_dark, modify_named_font, INTERNAL_PAD
from app_locale import _


@dataclasses.dataclass
class LicenseMetadata:
    """
    Metadata about the license used by the application
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


class AboutDialog(ModalDialog):
    """
    Display metadata about the application in a modal dialog.
    """
    def __init__(self, parent, about: AboutMetadata, iconpath=None):
        self.about = about
        title = _("About {}").format(about.app_name).strip()
        super().__init__(parent, title=title, iconpath=iconpath, class_="AboutBox")

    def init_styles(self):
        background = self.style.lookup("TLabel", "background")
        dark_mode = is_dark(f"{background}")
        self.style.configure("System.TLabel", font="TkDefaultFont")
        self.style.configure(
            "About_URL.System.TLabel",
            foreground="#66CCFF" if dark_mode else "#0000EE"
        )

    def update_screen(self):
        pass

    def on_save(self):
        pass

    def create_widgets(self):
        frame = ttk.Frame(self, padding=INTERNAL_PAD)
        frame.grid()
        notebook = ttk.Notebook(frame)
        notebook.grid(sticky=tk.W+tk.E+tk.N, pady=INTERNAL_PAD)
        tab1 = ttk.Frame(notebook)
        base_font = font.nametofont("TkDefaultFont")
        large_font = modify_named_font(
            "TkDefaultFont", size=base_font.actual()["size"]+4
        )
        if self.icon is not None:
            ttk.Label(
                tab1, image=self.icon
            ).grid()
        if self.about.app_name != "":
            ttk.Label(
                tab1, text=self.about.app_name, font=large_font
            ).grid(row=1)
        if self.about.version != "":
            version = _("Version {}").format(self.about.version)
            ttk.Label(
                tab1, text=version, font=base_font
            ).grid(row=2)
        if self.about.author != "":
            if self.about.copyright_year != "":
                copyright_text = f"© {self.about.copyright_year} {self.about.author}"
            else:
                copyright_text = f"© {self.about.author}"
            ttk.Label(
                tab1, text=copyright_text, font=base_font
            ).grid(row=3)
        if self.about.url != "":
            link1style = UrlLabel.test_web_protocol(
                self.about.url, "About_URL.System.TLabel", "System.TLabel"
            )
            UrlLabel(
                tab1, text=_("Source Code"), url=self.about.url,
                style=link1style, font=base_font, show_tooltip=True
            ).grid(row=4)
        if self.about.description != "":
            ttk.Label(
                tab1, text=self.about.description, wraplength=450, font=base_font
            ).grid(row=5)
        notebook.add(tab1, text=self.title(), sticky=tk.N, padding=INTERNAL_PAD)
        if self.about.license is not None:
            tab2 = ttk.Frame(notebook)
            if self.about.license.full_license != "":
                license_text = [
                    line.replace(
                        "\n", " "
                    ) for line in self.about.license.full_license.split("\n\n")
                ]
                text = tk.Text(
                    tab2, font=base_font, height=14, width=55, wrap=tk.WORD,
                    undo=False, relief=tk.FLAT
                )
                text.insert(tk.END, "\n\n".join(license_text))
                text.config(state=tk.DISABLED)
                text.grid(row=0, column=0)
                text_scroller = ttk.Scrollbar(tab2, orient=tk.VERTICAL)
                text_scroller.grid(row=0, column=1, sticky=tk.N+tk.S)
                text.config(yscrollcommand=text_scroller.set)
                text_scroller.config(command=text.yview)
            elif self.about.license.license_name != "":
                tk.Label(
                    tab2, font=base_font, text=self.about.license.license_name
                ).grid(row=0, pady=INTERNAL_PAD)
                if self.about.license.license_url != "":
                    link2style = UrlLabel.test_web_protocol(
                        self.about.license.license_url,
                        "About_URL.System.TLabel", "System.TLabel"
                    )
                    UrlLabel(
                        tab2, text=_("Full license text available here"),
                        url=self.about.license.license_url, style=link2style,
                        show_tooltip=True
                    ).grid(row=1, pady=INTERNAL_PAD)
            notebook.add(tab2, text=_("License"), sticky=tk.N)
        notebook.enable_traversal()
        ttk.Button(
            frame, text=_("Close"), command=self.dismiss, style='Accent.TButton'
        ).grid(sticky=tk.E)
