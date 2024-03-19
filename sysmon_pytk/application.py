# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
System monitor.
"""

import sys
import tkinter as tk
from socket import gethostname
from tkinter import font, ttk

import psutil

from . import _common, about
from .app_locale import get_translator, reload_translated_modules
from .file_utils import get_full_path, settings_path
from .modals import CpuDialog, DiskUsageDialog, MemUsageDialog, SettingsDialog, TempDetailsDialog
from .modals.about_modal import AboutDialog, AboutMetadata, LicenseMetadata
from .settings import Settings
from .style_manager import StyleManager
from .widgets import Meter, ToolTip

_ = get_translator()

APP_TITLE = _("System Monitor")


class Application(tk.Tk):  # pylint: disable=too-many-instance-attributes
    """
    System monitor application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.title(APP_TITLE)
        self.iconphoto(False, tk.PhotoImage(file=get_full_path("images/icon.png")))
        self.read_settings()
        self._name = tk.StringVar()
        self._ip_addr = tk.StringVar()
        self._uptime = tk.StringVar()
        self._processes = tk.StringVar()
        self._update_job = None
        StyleManager.init_theme(self, self.settings)
        frame = self._init_frame()
        self._add_variable_label(frame, self._name, 1, 1)
        self._add_variable_label(frame, self._ip_addr, 1, 2)
        self._add_variable_label(frame, self._processes, 1, 3)
        self._add_variable_label(frame, self._uptime, 1, 4)
        self._add_cpu_meter(frame)
        self._add_temp_meter(frame)
        self._add_ram_meter(frame)
        self._add_disk_meter(frame)
        self._add_sizegrip(frame)
        self.build_menu()
        self.bind_events()
        self.update_screen()

    def read_settings(self, *_args):
        """
        Read application settings from configuration file.
        """
        self.settings = Settings(settings_path())
        self.call("wm", "attributes", ".", "-topmost", f"{self.settings.get_always_on_top()}")

    def _init_frame(self) -> ttk.Frame:
        frame = ttk.Frame(self)
        frame.grid(sticky=tk.NSEW)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)
        return frame

    def _add_variable_label(self, frame, textvariable, row, column):
        base_font = StyleManager.get_base_font()
        ttk.Label(
            frame, textvariable=textvariable, font=base_font, anchor=tk.CENTER
        ).grid(
            row=row, column=column, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )

    def _add_cpu_meter(self, frame: ttk.Frame):
        self._cpu_meter = Meter(
            frame, width=220, height=165, unit="%", label=_("CPU Usage")
        )
        self._cpu_meter.grid(
            row=2, column=1, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )
        if psutil.cpu_count() > 1:
            self._cpu_meter.configure(cursor="hand2")
            ToolTip(self._cpu_meter, _("Click for per-CPU usage"))

    def _add_temp_meter(self, frame: ttk.Frame):
        self._temp_meter = Meter(
            frame, width=220, height=165, unit="°C", blue=15, label=_("Temperature")
        )
        self._temp_meter.grid(
            row=2, column=2, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )
        self._temp_meter.configure(cursor="hand2")
        ToolTip(self._temp_meter, _("Click for detailed temperature readings"))

    def _add_ram_meter(self, frame: ttk.Frame):
        self._ram_meter = Meter(
            frame, width=220, height=165, unit="%", label=_("RAM Usage")
        )
        self._ram_meter.grid(
            row=2, column=3, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )
        self._ram_meter.configure(cursor="hand2")
        ToolTip(self._ram_meter, _("Click for detailed memory statistics"))

    def _add_disk_meter(self, frame: ttk.Frame):
        self._disk_meter = Meter(
            frame, width=220, height=165, unit="%", label=_("Disk Usage: /"),
            red=100 - _common.DISK_ALERT_LEVEL,
            yellow=_common.DISK_ALERT_LEVEL - _common.DISK_WARN_LEVEL
        )
        self._disk_meter.grid(
            row=2, column=4, sticky=tk.NSEW, pady=(_common.INTERNAL_PAD, 0)
        )
        self._disk_meter.configure(cursor="hand2")
        ToolTip(
            self._disk_meter, _("Click for usage details of each mount point")
        )

    def _add_sizegrip(self, frame: ttk.Frame):
        ttk.Sizegrip(frame).grid(
            row=3, column=4, sticky=tk.SE, padx=_common.INTERNAL_PAD/2,
            pady=(0, _common.INTERNAL_PAD/2)
        )

    def build_menu(self):
        """
        Build the application menu.
        """
        self.option_add("*tearOff", False)  # Fix menus
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        menu_bar = tk.Menu(top, relief=tk.FLAT)
        file_menu = tk.Menu(menu_bar, font=font.nametofont("TkMenuFont"), relief=tk.SOLID)

        menu_bar.add_cascade(
            label=_("File"), menu=file_menu, font=font.nametofont("TkMenuFont")
        )
        file_menu.add_command(
            label=_("About"), accelerator=_("Ctrl+A"), command=self._on_about
        )
        file_menu.add_command(
            label=_("Preferences"), accelerator=_("Ctrl+Shift+P"),
            command=self._on_settings
        )
        file_menu.add_command(
            label=_("Restart"), accelerator=_("Ctrl+R"), command=self._on_restart
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=_("Quit"), accelerator=_("Ctrl+Q"), command=lambda : sys.exit(0)
        )
        top["menu"] = menu_bar
        # bind keypress events for menu here
        self.bind("<Control-KeyPress-a>", self._on_about)
        self.bind("<Control-Shift-KeyPress-P>", self._on_settings)
        self.bind("<Control-KeyPress-r>", self._on_restart)
        self.bind("<Control-KeyPress-q>", lambda : sys.exit(0))

    def bind_events(self):
        """
        Set up bindings for app events.
        """
        self.bind("<<SettingsChanged>>", self.read_settings)
        self.bind("<<LanguageChanged>>", self._on_language)
        self.bind("<<FontChanged>>", self._on_restart)
        if psutil.cpu_count() > 1:
            self._cpu_meter.bind("<Button-1>", self._on_cpu_details)
        self._temp_meter.bind("<Button-1>", self._on_temp_details)
        self._ram_meter.bind("<Button-1>", self._on_mem_details)
        self._disk_meter.bind("<Button-1>", self._on_disk_usage)

    def _on_language(self, *_args):
        """
        Update the selected language.
        """
        reload_translated_modules()
        self._on_restart()

    def _on_about(self, *_args):
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

    def _on_restart(self, *_args):
        if self._update_job is not None:
            self.after_cancel(self._update_job)
            self._update_job = None
        self.destroy()
        self.__init__(self.parent)  # pylint: disable=unnecessary-dunder-call

    def _on_cpu_details(self, *_args):
        """
        Open CPU Details.
        """
        CpuDialog(
            self, title=_("{} :: CPU Details").format(APP_TITLE),
            iconpath=get_full_path("images/icon.png")
        )

    def _on_temp_details(self, *_args):
        """
        Open Temperature Details.
        """
        TempDetailsDialog(
            self, title=_("{} :: Temperature Details").format(APP_TITLE),
            iconpath=get_full_path("images/icon.png")
        )

    def _on_mem_details(self, *_args):
        """
        Open Memory Usage.
        """
        MemUsageDialog(
            self, title=_("{} :: Memory Usage").format(APP_TITLE),
            iconpath=get_full_path("images/icon.png")
        )

    def _on_disk_usage(self, *_args):
        """
        Open Disk Usage.
        """
        DiskUsageDialog(
            self, title=_("{} :: Disk Usage").format(APP_TITLE),
            iconpath=get_full_path("images/icon.png")
        )

    def _on_settings(self, *_args):
        """
        Open Settings and process any changes afterward.
        """
        SettingsDialog(
            self.settings, self, _("{} Preferences").format(APP_TITLE),
            iconpath=get_full_path("images/icon.png")
        )
        StyleManager.update_by_dark_mode(self, self.settings)
        self._cpu_meter.update_for_dark_mode()
        self._temp_meter.update_for_dark_mode()
        self._ram_meter.update_for_dark_mode()
        self._disk_meter.update_for_dark_mode()

    def update_screen(self):
        """
        Update the screen.
        """
        self._cpu_meter.set_value(psutil.cpu_percent(interval=None))
        self._temp_meter.set_value(_common.cpu_temp())
        self._ram_meter.set_value(psutil.virtual_memory().percent)
        self._disk_meter.set_value(psutil.disk_usage("/").percent)
        self._name.set(_("Hostname: {}").format(gethostname()))
        self._ip_addr.set(_("IP Address: {}").format(_common.net_addr()))
        self._processes.set(_("Processes: {}").format(len(psutil.pids())))
        self._uptime.set(_("Uptime: {}").format(_common.system_uptime()))
        self._update_job = self.after(
            _common.REFRESH_INTERVAL, self.update_screen
        )
