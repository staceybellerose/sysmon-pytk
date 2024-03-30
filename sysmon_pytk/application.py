# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
System monitor.
"""

from __future__ import annotations

import sys
import tkinter as tk
from socket import gethostname
from tkinter import font, ttk
from typing import TYPE_CHECKING

import psutil

from . import _common, about
from .app_locale import get_translator, reload_translated_modules
from .file_utils import get_full_path, settings_path
from .modals import SettingsDialog
from .modals.about_modal import AboutDialog, AboutMetadata, LicenseMetadata
from .settings import Settings
from .style_manager import StyleManager
from .widgets import TempToolTip, ToolTip
from .widgets.meters import CpuMeter, DiskMeter, RamMeter, TempMeter

if TYPE_CHECKING:
    from tkinter import Variable

_ = get_translator()

APP_TITLE = _("System Monitor")


class Application(tk.Tk):
    """
    System monitor application.

    Attributes
    ----------
    _name : StringVar
        The hostname of the system.
    _ip_addr : StringVar
        The IP Address of the system.
    _uptime : StringVar
        The current uptime of the system.
    _processes : StringVar
        The current process count of the system.
    _update_job : str
        The ID of the scheduled job to update the screen.
    _menu_icons : dict[str, PhotoImage]
        The icons used in the menu.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.iconphoto(False, tk.PhotoImage(file=get_full_path("images/icon.png")))
        self.read_settings()
        self._name = tk.StringVar()
        self._ip_addr = tk.StringVar()
        self._uptime = tk.StringVar()
        self._processes = tk.StringVar()
        self._update_job: str | None = None
        StyleManager.init_theme(self, self.settings)
        self.create_widgets()
        self._load_menu_images()
        self.build_menu()
        self.bind_events()
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        self.update_screen()

    def read_settings(self, *_args) -> None:
        """
        Read application settings from configuration file.
        """
        self.settings = Settings(settings_path())
        self.call("wm", "attributes", ".", "-topmost", f"{self.settings.always_on_top}")

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the main application window.
        """
        frame = ttk.Frame(self)
        frame.grid(sticky=tk.NSEW)
        for row in [1, 2]:
            frame.rowconfigure(row, weight=1)
        for column in [1, 2, 3, 4]:
            frame.columnconfigure(column, weight=1)
        self._add_variable_label(frame, self._name, 1, 1)
        ip_label = self._add_variable_label(frame, self._ip_addr, 1, 2)
        ToolTip(ip_label, _("Click to copy IP Address to clipboard"))
        ip_label.bind("<Button-1>", self._on_click_ip_address)
        self._add_variable_label(frame, self._processes, 1, 3)
        self._add_variable_label(frame, self._uptime, 1, 4)
        self._add_meters(frame)
        self._add_sizegrip(frame)

    @classmethod
    def _add_variable_label(
        cls, frame: ttk.Frame, textvariable: Variable, row: int, column: int
    ) -> ttk.Label:
        base_font = StyleManager.get_base_font()
        label = ttk.Label(
            frame, textvariable=textvariable, font=base_font, anchor=tk.CENTER
        )
        label.grid(
            row=row, column=column, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )
        return label

    def _add_meters(self, frame: ttk.Frame) -> None:
        CpuMeter(frame, width=220, height=165).grid(
            row=2, column=1, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )
        TempMeter(frame, width=220, height=165).grid(
            row=2, column=2, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )
        RamMeter(frame, width=220, height=165).grid(
            row=2, column=3, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )
        DiskMeter(frame, width=220, height=165).grid(
            row=2, column=4, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )

    @classmethod
    def _add_sizegrip(cls, frame: ttk.Frame) -> None:
        ttk.Sizegrip(frame).grid(
            row=3, column=4, sticky=tk.SE, padx=_common.INTERNAL_PAD/2,
            pady=(0, _common.INTERNAL_PAD/2)
        )

    def _load_menu_images(self) -> None:
        self._menu_icons = {
            "about": tk.PhotoImage(file=get_full_path("images/internet-group-chat.png")),
            "preferences": tk.PhotoImage(file=get_full_path("images/preferences-system.png")),
            "restart": tk.PhotoImage(file=get_full_path("images/view-refresh.png")),
            "quit": tk.PhotoImage(file=get_full_path("images/blank.png"))
        }

    def build_menu(self) -> None:
        """
        Build the application menu.
        """
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        menu_bar = tk.Menu(
            top, relief=tk.FLAT, activeborderwidth=0,
            font=font.nametofont("TkMenuFont"),
            background=StyleManager.get_menu_background(),
            foreground=StyleManager.get_menu_foreground()
        )
        file_menu = tk.Menu(
            menu_bar, relief=tk.FLAT, activeborderwidth=0,
            font=font.nametofont("TkMenuFont"),
            background=StyleManager.get_menu_background(),
            foreground=StyleManager.get_menu_foreground()
        )

        menu_bar.add_cascade(
            label=_("File"), menu=file_menu,
        )
        file_menu.add_command(
            label=_("About"), accelerator=_("Ctrl+A"), command=self._on_about,
            compound=tk.LEFT, image=self._menu_icons["about"]
        )
        file_menu.add_command(
            label=_("Preferences"), accelerator=_("Ctrl+Shift+P"), command=self._on_settings,
            compound=tk.LEFT, image=self._menu_icons["preferences"]
        )
        file_menu.add_command(
            label=_("Restart"), accelerator=_("Ctrl+R"), command=self._on_restart,
            compound=tk.LEFT, image=self._menu_icons["restart"]
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=_("Quit"), accelerator=_("Ctrl+Q"), command=lambda: sys.exit(0),
            compound=tk.LEFT, image=self._menu_icons["quit"]
        )
        top["menu"] = menu_bar
        # bind keypress events for menu here
        self.bind("<Control-KeyPress-a>", self._on_about)
        self.bind("<Control-Shift-KeyPress-P>", self._on_settings)
        self.bind("<Control-KeyPress-r>", self._on_restart)
        self.bind("<Control-KeyPress-q>", lambda _x: sys.exit(0))

    def bind_events(self) -> None:
        """
        Set up bindings for app events.
        """
        self.bind("<<SettingsChanged>>", self.read_settings)
        self.bind("<<LanguageChanged>>", self._on_language)
        self.bind("<<FontChanged>>", self._on_restart)

    def _on_click_ip_address(self, event: tk.Event) -> None:
        self.clipboard_clear()
        self.clipboard_append(_common.net_addr())
        TempToolTip(self, _("Copied!"), (event.x_root, event.y_root), 5000)

    def _on_language(self, *_args) -> None:
        """
        Update the selected language.
        """
        reload_translated_modules()
        self._on_restart()

    def _on_about(self, *_args) -> None:
        """
        Open About box.
        """
        metadata = AboutMetadata(
            about.__app_name__, about.__version__, about.__author__,
            about.__copyright_year__, about.__summary__, about.__url__,
            LicenseMetadata(
                about.__full_license__, about.__license__, about.__license_url__
            )
        )
        AboutDialog(self, metadata, iconpath=get_full_path("images/icon.png"))

    def _on_restart(self, *_args) -> None:
        if self._update_job is not None:
            self.after_cancel(self._update_job)
            self._update_job = None
        self.destroy()
        self.__init__()  # type: ignore[misc] # pylint: disable=unnecessary-dunder-call

    def _on_settings(self, *_args) -> None:
        """
        Open Settings and process any changes afterward.
        """
        SettingsDialog(
            self.settings, self, _("{} Preferences").format(APP_TITLE),
            iconpath=get_full_path("images/icon.png")
        )
        StyleManager.update_by_dark_mode(self, self.settings)

    def update_screen(self) -> None:
        """
        Update the screen.
        """
        self._name.set(_("Hostname: {}").format(gethostname()))
        self._ip_addr.set(_("IP Address: {}").format(_common.net_addr()))
        self._processes.set(_("Processes: {}").format(len(psutil.pids())))
        self._uptime.set(_("Uptime: {}").format(_common.system_uptime()))
        self._update_job = self.after(
            _common.REFRESH_INTERVAL, self.update_screen
        )
