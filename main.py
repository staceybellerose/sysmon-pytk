#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
System monitor.
"""

import os
import sys
import tkinter as tk
from socket import gethostname
from tkinter import ttk, font

import darkdetect
import psutil

import _common
import about
import tkabout
from settings import Settings
from tkmeter import Meter
from tkmodal import CpuDialog, TempDetailsDialog, MemUsageDialog, DiskUsageDialog, SettingsDialog
from widgets import ToolTip
from app_locale import _

APP_TITLE = _("System Monitor")


class Application(tk.Tk):  # pylint: disable=too-many-instance-attributes
    """
    System monitor application.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title(APP_TITLE)
        self.iconphoto(False, tk.PhotoImage(file=_common.get_full_path("icon.png")))
        self.read_settings()
        self._name = tk.StringVar()
        self._ip_addr = tk.StringVar()
        self._uptime = tk.StringVar()
        self._processes = tk.StringVar()
        self.init_theme()
        self.init_fonts()
        self.create_widgets()
        self.build_menu()
        self.bind_events()
        self.update_screen()

    def read_settings(self):
        """
        Read application settings from configuration file.
        """
        self.settings = Settings(_common.SETTINGS_FILE)
        if self.settings.get_always_on_top():
            self.call('wm', 'attributes', '.', '-topmost', '1')
        else:
            self.call('wm', 'attributes', '.', '-topmost', '0')

    def init_theme(self):
        """
        Initialize the display theme.
        """
        dark_mode = darkdetect.isDark()
        if self.settings.get_theme() == "Dark":
            dark_mode = True
        elif self.settings.get_theme() == "Light":
            dark_mode = False
        elif self.settings.get_theme() == "Same as System":
            dark_mode = darkdetect.isDark()
        self.tk.call("source", _common.get_full_path("azure/azure.tcl"))
        self.tk.call("set_theme", "dark" if dark_mode else "light")
        base_font = font.nametofont("TkDefaultFont")
        style = ttk.Style()
        style.configure("Safe.TLabel", foreground="#0a0" if dark_mode else "#090")
        style.configure("Warn.TLabel", foreground="#ff2" if dark_mode else "#aa0")
        style.configure("Alert.TLabel", foreground="#f22" if dark_mode else "#c00")
        style.configure("TButton", font=base_font)
        style.configure("TRadiobutton", font=base_font)
        style.configure("TLabelFrame", font=base_font)

    def init_fonts(self):
        """
        Initialize the fonts to be used.
        """
        base_font = font.nametofont("TkDefaultFont")
        text_font = font.nametofont("TkTextFont")
        menu_font = font.nametofont("TkMenuFont")
        fixed_font = font.nametofont("TkFixedFont")
        if self.settings.regular_font.get_name() != "":
            base_font.configure(
                family=self.settings.regular_font.get_name(),
                size=self.settings.regular_font.get_size(),
                weight=self.settings.regular_font.get_weight(),
                slant=self.settings.regular_font.get_slant(),
                underline=self.settings.regular_font.get_underline(),
                overstrike=self.settings.regular_font.get_overstrike()
            )
            text_font.configure(
                family=self.settings.regular_font.get_name(),
                size=self.settings.regular_font.get_size(),
                weight=self.settings.regular_font.get_weight(),
                slant=self.settings.regular_font.get_slant(),
                underline=self.settings.regular_font.get_underline(),
                overstrike=self.settings.regular_font.get_overstrike()
            )
            menu_font.configure(
                family=self.settings.regular_font.get_name(),
                size=self.settings.regular_font.get_size(),
                weight=self.settings.regular_font.get_weight(),
                slant=self.settings.regular_font.get_slant(),
                underline=self.settings.regular_font.get_underline(),
                overstrike=self.settings.regular_font.get_overstrike()
            )
        else:
            base_font.configure(family=_common.MAIN_FONT_FAMILY, size=12)
            text_font.configure(family=_common.MAIN_FONT_FAMILY, size=12)
            menu_font.configure(family=_common.MAIN_FONT_FAMILY, size=12)
        if self.settings.fixed_font.get_name() != "":
            fixed_font.configure(
                family=self.settings.fixed_font.get_name(),
                size=self.settings.fixed_font.get_size(),
                weight=self.settings.fixed_font.get_weight(),
                slant=self.settings.fixed_font.get_slant(),
                underline=self.settings.fixed_font.get_underline(),
                overstrike=self.settings.fixed_font.get_overstrike()
            )
        else:
            fixed_font.configure(family=_common.FIXED_FONT_FAMILY, size=12)

    def create_widgets(self):
        """
        Create the widgets to be displayed in the main application window.
        """
        frame = ttk.Frame(self)
        frame.grid()
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.columnconfigure(4, weight=1)

        basefont = font.nametofont("TkDefaultFont")
        ttk.Label(
            frame, textvariable=self._name, font=basefont
        ).grid(row=1, column=1, sticky=tk.S, ipady=_common.INTERNAL_PAD)
        ttk.Label(
            frame, textvariable=self._ip_addr, font=basefont
        ).grid(row=1, column=2, sticky=tk.S, ipady=_common.INTERNAL_PAD)
        ttk.Label(
            frame, textvariable=self._processes, font=basefont
        ).grid(row=1, column=3, sticky=tk.S, ipady=_common.INTERNAL_PAD)
        ttk.Label(
            frame, textvariable=self._uptime, font=basefont
        ).grid(row=1, column=4, sticky=tk.S, ipady=_common.INTERNAL_PAD)

        self._cpu_meter = Meter(
            frame, width=220, height=165, unit="%", label=_("CPU Usage")
        )
        self._cpu_meter.grid(row=2, column=1, sticky=tk.N, ipady=_common.INTERNAL_PAD)
        if psutil.cpu_count() > 1:
            self._cpu_meter.configure(cursor="hand2")
            ToolTip(self._cpu_meter, _('Click for per-CPU usage'))

        self._temp_meter = Meter(
            frame, width=220, height=165, unit="°C", blue=15,
            label=_("Temperature")
        )
        self._temp_meter.grid(row=2, column=2, sticky=tk.N, ipady=_common.INTERNAL_PAD)
        self._temp_meter.configure(cursor="hand2")
        ToolTip(self._temp_meter, _('Click for detailed temperature readings'))

        self._ram_meter = Meter(
            frame, width=220, height=165, unit="%", label=_("RAM Usage")
        )
        self._ram_meter.grid(row=2, column=3, sticky=tk.N, ipady=_common.INTERNAL_PAD)
        self._ram_meter.configure(cursor="hand2")
        ToolTip(self._ram_meter, _('Click for detailed memory statistics'))

        self._disk_meter = Meter(
            frame, width=220, height=165, unit="%", label=_("Disk Usage: /"),
            red=100 - _common.DISK_ALERT_LEVEL,
            yellow=_common.DISK_ALERT_LEVEL - _common.DISK_WARN_LEVEL
        )
        self._disk_meter.grid(row=2, column=4, sticky=tk.N, ipady=_common.INTERNAL_PAD)
        self._disk_meter.configure(cursor="hand2")
        ToolTip(self._disk_meter, _('Click for usage details of each mount point'))

    def build_menu(self):
        """
        Build the application menu.
        """
        self.option_add("*tearOff", False)  # Fix menus
        top = self.winfo_toplevel()
        menu_bar = tk.Menu(top)
        file_menu = tk.Menu(menu_bar, font=tk.font.nametofont("TkMenuFont"))

        menu_bar.add_cascade(
            label=_('File'), menu=file_menu, underline=0,
            font=tk.font.nametofont("TkMenuFont")
        )
        file_menu.add_command(
            label=_('About'), accelerator=_("Ctrl+A"), underline=0,
            command=self._on_about
        )
        file_menu.add_command(
            label=_('Preferences'), accelerator=_("Ctrl+Shift+P"), underline=0,
            command=self._on_settings
        )
        file_menu.add_command(
            label=_('Restart'), accelerator=_("Ctrl+R"), underline=0,
            command=self._on_restart
        )
        file_menu.add_separator()
        file_menu.add_command(
            label=_('Quit'), accelerator=_("Ctrl+Q"), underline=0,
            command=self._on_quit
        )
        top['menu'] = menu_bar
        # bind keypress events for menu here
        self.bind("<Control-KeyPress-a>", self._on_about)
        self.bind("<Control-Shift-KeyPress-P>", self._on_settings)
        self.bind("<Control-KeyPress-r>", self._on_restart)
        self.bind("<Control-KeyPress-q>", self._on_quit)

    def bind_events(self):
        """
        Set up bindings for app events.
        """
        self.bind("<<SettingsChanged>>", self.apply_settings)
        self.bind("<<LanguageChanged>>", self._on_restart)
        self.bind("<<FontChanged>>", self._on_restart)
        if psutil.cpu_count() > 1:
            self._cpu_meter.bind("<Button-1>", self._on_cpu_details)
        self._temp_meter.bind("<Button-1>", self._on_temp_details)
        self._ram_meter.bind("<Button-1>", self._on_mem_details)
        self._disk_meter.bind("<Button-1>", self._on_disk_usage)

    def _on_about(self, *_args):
        metadata = tkabout.AboutMetadata(
            about.__app_name__, about.__version__, about.__author__,
            about.__copyright_year__, about.__summary__, about.__url__,
            tkabout.LicenseMetadata(
                about.__full_license__, about.__license__, about.__license_url__
            )
        )
        tkabout.AboutDialog(self, metadata, iconpath=_common.get_full_path("icon-lg.png"))

    def _on_quit(self, *_args):
        sys.exit(0)

    def _on_restart(self, *_args):
        os.execl(sys.executable, 'python3', __file__, *sys.argv[1:])

    def _on_cpu_details(self, *_args):
        CpuDialog(
            self, title=_("{} :: CPU Details").format(APP_TITLE),
            iconpath=_common.get_full_path("icon.png")
        )

    def _on_temp_details(self, *_args):
        TempDetailsDialog(
            self, title=_("{} :: Temperature Details").format(APP_TITLE),
            iconpath=_common.get_full_path("icon.png")
        )

    def _on_mem_details(self, *_args):
        MemUsageDialog(
            self, title=_("{} :: Memory Usage").format(APP_TITLE),
            iconpath=_common.get_full_path("icon.png")
        )

    def _on_disk_usage(self, *_args):
        DiskUsageDialog(
            self, title=_("{} :: Disk Usage").format(APP_TITLE),
            iconpath=_common.get_full_path("icon.png")
        )

    def _on_settings(self, *_args):
        SettingsDialog(
            self.settings, self, _("{} Preferences").format(APP_TITLE),
            iconpath=_common.get_full_path("icon.png")
        )
        if self.settings.get_theme() == "Dark":
            dark_mode = True
        elif self.settings.get_theme() == "Light":
            dark_mode = False
        elif self.settings.get_theme() == "Same as System":
            dark_mode = darkdetect.isDark()
        self.tk.call("set_theme", "dark" if dark_mode else "light")
        self._cpu_meter.update_for_dark_mode()
        self._temp_meter.update_for_dark_mode()
        self._ram_meter.update_for_dark_mode()
        self._disk_meter.update_for_dark_mode()
        style = ttk.Style()
        style.configure("Safe.TLabel", foreground="#0a0" if dark_mode else "#090")
        style.configure("Warn.TLabel", foreground="#ff2" if dark_mode else "#aa0")
        style.configure("Alert.TLabel", foreground="#f22" if dark_mode else "#c00")

    def update_screen(self):
        """
        Update the screen.
        """
        self._cpu_meter.set_value(psutil.cpu_percent(interval=None))
        self._temp_meter.set_value(_common.cpu_temp())
        self._ram_meter.set_value(psutil.virtual_memory().percent)
        self._disk_meter.set_value(psutil.disk_usage('/').percent)
        self._name.set(_("Hostname: {}").format(gethostname()))
        self._ip_addr.set(_("IP Address: {}").format(_common.net_addr()))
        self._processes.set(_("Processes: {}").format(len(psutil.pids())))
        self._uptime.set(_("Uptime: {}").format(_common.system_uptime()))
        self.after(_common.REFRESH_INTERVAL, self.update_screen)

    def apply_settings(self, *_args):
        """
        Apply the new settings to the application.
        """
        self.read_settings()


if __name__ == "__main__":
    app = Application()
    app.update()
    app.minsize(app.winfo_width(), app.winfo_height())
    app.mainloop()
