# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Modal dialogs.
"""

from abc import abstractmethod
from typing import Optional, Literal, final
import tkinter as tk
from tkinter import ttk, font, Event
from tkinter.font import Font

import psutil

import _common
from settings import Settings, FontDescription
from tkmeter import Meter
from widgets import DropDown, ScaleSpinner
from app_locale import _, LANGUAGES


class ModalDialog(tk.Toplevel):
    """
    Base class for modal dialogs.

    Attributes
    ----------
    parent : Misc, optional
        The parent widget.
    iconpath : str, optional
        The path to the icon to display in the window title bar.
    internal_frame : Frame
        A `Frame` to manage the widgets added to the dialog.
    """

    def __init__(
        self, parent=None, title: Optional[str] = None,
        iconpath: Optional[str] = None, class_: str = "ModalDialog"
    ):
        """
        Construct a modal dialog.

        Parameters
        ----------
        parent : Misc, optional
            The parent widget.
        title : str, optional
            The title to display in the window title bar.
        iconpath : str, optional
            The path to the icon to display in the window title bar.
        class_ : str, default: "ModalDialog"
            The class name of this modal dialog, used with the option database
            for styling.
        """
        super().__init__(parent, class_=class_)
        self.parent = parent
        self.title(title)
        self.icon = None
        self.iconpath = iconpath
        if iconpath is not None:
            self.icon = tk.PhotoImage(file=iconpath)
            self.iconphoto(False, self.icon)
        self.style = ttk.Style()
        self.init_styles()
        self.create_widgets()
        self.update_screen()
        self.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.bind("<KeyPress-Escape>", self.dismiss)
        self.bind("<KeyPress-Return>", self.save_and_dismiss)
        self.bind("<KeyPress-KP_Enter>", self.save_and_dismiss)
        self.transient(parent)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    @final
    def dismiss(self, *_args):
        """
        Dismiss the modal dialog.

        This should be bound to Cancel and Close buttons in subclasses.
        """
        self.grab_release()
        self.destroy()

    @final
    def save_and_dismiss(self, *_args):
        """
        Save what was entered in the modal dialog and dismiss it.

        This should be bound to OK and Save buttons in subclasses.
        """
        self.on_save()
        self.dismiss()

    @abstractmethod
    def on_save(self):
        """
        Save what was entered in the modal dialog.
        """

    @abstractmethod
    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.
        """

    @abstractmethod
    def create_widgets(self):
        """
        Create the widgets to be displayed in the modal dialog.
        """

    @abstractmethod
    def update_screen(self):
        """
        Update the modal dialog window.
        """


class CpuDialog(ModalDialog):
    """
    Display individual CPU core usage details in a modal dialog.

    Attributes
    ----------
    cpu_count : int
        The number of logical CPUs in the system.
    """

    def on_save(self):
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.

        This dialog does not require additional styles.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self.cpu_count = psutil.cpu_count()
        cpu_model = _common.get_processor_name()
        max_columns = 4
        frame = ttk.Frame(self)
        frame.grid()
        base_font = font.nametofont("TkDefaultFont")
        large_font = _common.modify_named_font(
            "TkDefaultFont", size=base_font.actual()["size"]+4
        )
        ttk.Label(
            frame, text=cpu_model, font=large_font
        ).grid(columnspan=max_columns)
        ttk.Label(
            frame, text=_("per-core CPU Usage"), font=large_font
        ).grid(columnspan=max_columns, row=1)
        row = 2
        col = 0
        self._meters = []
        for core in range(self.cpu_count):
            meter = Meter(
                frame, width=220, height=165, unit="%",
                label=_("CPU #{}").format(core)
            )
            meter.grid(row=row, column=col, sticky=tk.N, ipady=_common.INTERNAL_PAD)
            self._meters.append(meter)
            col += 1
            if col == max_columns:
                col = 0
                row += 1
        row += 1
        ttk.Label(
            frame, text=_("per-core CPU Frequency (in MHz)"),
            font=large_font
        ).grid(columnspan=max_columns, row=row)
        row += 1
        self._freqmeters = []
        freqs = psutil.cpu_freq(percpu=True)
        for core in range(self.cpu_count):
            meter = Meter(
                frame, width=220, height=165, unit="", label=_("CPU #{}").format(core),
                min_value=freqs[core].min, max_value=freqs[core].max
            )
            meter.grid(row=row, column=col, sticky=tk.N, ipady=_common.INTERNAL_PAD)
            self._freqmeters.append(meter)
            col += 1
            if col == max_columns:
                col = 0
                row += 1
        row += 1
        ttk.Button(
            frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=row, column=1, sticky=tk.E, columnspan=max_columns,
            pady=_common.INTERNAL_PAD, padx=_common.INTERNAL_PAD
        )

    def update_screen(self):
        """
        Update the modal dialog window.
        """
        usage = psutil.cpu_percent(interval=None, percpu=True)
        for core in range(self.cpu_count):
            self._meters[core].set_value(usage[core])
        freqs = psutil.cpu_freq(percpu=True)
        for core in range(self.cpu_count):
            self._freqmeters[core].set_value(freqs[core].current)
        self.after(_common.REFRESH_INTERVAL, self.update_screen)


class TempDetailsDialog(ModalDialog):
    """
    Display detailed temperature readings in a modal dialog.
    """

    def on_save(self):
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.

        This dialog does not require additional styles.
        """

    def create_widgets(self):
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self._readings = []
        frame = ttk.Frame(self)
        frame.grid()
        base_font = font.nametofont("TkDefaultFont")
        large_font = _common.modify_named_font(
            "TkDefaultFont", size=base_font.actual()["size"]+4
        )
        bold_font = _common.modify_named_font(
            "TkDefaultFont", weight="bold"
        )
        ttk.Label(
            frame, text=_("Temperature Sensors"), font=large_font
        ).grid(columnspan=2)
        temps = psutil.sensors_temperatures()
        row = 0
        for name, entries in temps.items():
            ttk.Label(
                frame, text=name.upper(), anchor=tk.SW, font=bold_font
            ).grid(
                column=0, row=row, sticky=tk.W, ipady=_common.INTERNAL_PAD,
                padx=_common.INTERNAL_PAD
            )
            row += 1
            entryreadings = []
            for count, entry in enumerate(entries):
                entryreadings.append(tk.StringVar())
                entryreadings[count].set(self._format_entry(entry))
                ttk.Label(
                    frame, text=entry.label or name, anchor=tk.W, font=base_font
                ).grid(column=0, row=row, padx=_common.INTERNAL_PAD*2, sticky=tk.W)
                ttk.Label(
                    frame, textvariable=entryreadings[count], anchor=tk.W,
                    font=base_font
                ).grid(column=1, row=row, padx=_common.INTERNAL_PAD, sticky=tk.W)
                row += 1
            self._readings.append(entryreadings)
        ttk.Button(
            frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=row, column=1, sticky=tk.E,
            pady=_common.INTERNAL_PAD, padx=_common.INTERNAL_PAD
        )

    def update_screen(self):
        """
        Update the modal dialog window.
        """
        temps = psutil.sensors_temperatures()
        row = 0
        for _name, entries in temps.items():
            for count, entry in enumerate(entries):
                self._readings[row][count].set(self._format_entry(entry))
            row += 1
        self.after(_common.REFRESH_INTERVAL, self.update_screen)

    def _format_entry(self, entry):
        return _("{current}°C (high = {high}°C, critical = {critical}°C)").format(
            current=entry.current, high=entry.high, critical=entry.critical
        )


class MemUsageDialog(ModalDialog):
    """
    Display memory usage in a modal dialog.
    """

    def on_save(self):
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.

        This dialog does not require additional styles.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        self._names = []
        self._metrics = []
        self._swaps = []
        self._swap_metrics = []
        for count, item in enumerate(mem._asdict().items()):
            self._names.append(item[0])
            self._metrics.append(tk.StringVar())
        for count, item in enumerate(swap._asdict().items()):
            self._swaps.append(item[0])
            self._swap_metrics.append(tk.StringVar())
        frame = ttk.Frame(self)
        frame.grid()
        base_font = font.nametofont("TkDefaultFont")
        large_font = _common.modify_named_font(
            "TkDefaultFont", size=base_font.actual()["size"]+4
        )
        bold_font = _common.modify_named_font(
            "TkDefaultFont", weight="bold"
        )
        fixed_font = font.nametofont("TkFixedFont")
        ttk.Label(
            frame, text=_("Memory Statistics"), font=large_font
        ).grid(row=0, column=0, columnspan=5)
        ttk.Label(
            frame, text=_("Virtual Memory"), font=bold_font
        ).grid(row=1, column=0, columnspan=2)
        ttk.Label(frame, text="").grid(row=1, column=2)
        ttk.Label(
            frame, text=_("Swap Memory"), font=bold_font
        ).grid(row=1, column=3, columnspan=2)
        frame.columnconfigure(2, minsize=4*_common.INTERNAL_PAD)
        for count, name in enumerate(self._names):
            ttk.Label(
                frame, text=name.capitalize(), anchor=tk.W,
                font=base_font
            ).grid(row=count+2, column=0, sticky=tk.W, padx=_common.INTERNAL_PAD)
            ttk.Label(
                frame, textvariable=self._metrics[count], anchor=tk.E,
                font=fixed_font
            ).grid(row=count+2, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        for count, name in enumerate(self._swaps):
            ttk.Label(
                frame, text=name.capitalize(), anchor=tk.W,
                font=base_font
            ).grid(row=count+2, column=3, sticky=tk.W, padx=_common.INTERNAL_PAD)
            ttk.Label(
                frame, textvariable=self._swap_metrics[count],
                font=fixed_font, anchor=tk.E
            ).grid(row=count+2, column=4, sticky=tk.E, padx=_common.INTERNAL_PAD)
        ttk.Button(
            frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=max(len(self._names), len(self._swaps))+3, column=3, columnspan=2,
            sticky=tk.E, pady=_common.INTERNAL_PAD, padx=_common.INTERNAL_PAD
        )

    def update_screen(self):
        """
        Update the modal dialog window.
        """
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        for count, item in enumerate(mem._asdict().items()):
            self._metrics[count].set(
                _common.bytes2human(item[1]) if item[0] != "percent" else f"{item[1]}%"
            )
        for count, item in enumerate(swap._asdict().items()):
            self._swap_metrics[count].set(
                _common.bytes2human(item[1]) if item[0] != "percent" else f"{item[1]}%"
            )
        self.after(_common.REFRESH_INTERVAL, self.update_screen)


class DiskUsageDialog(ModalDialog):
    """
    Display disk usage in a modal dialog.
    """

    def on_save(self):
        """
        Save what was entered in the modal dialog.

        This dialog does not need a save feature.
        """

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.

        This dialog does not require additional styles.
        """

    def create_widgets(self):
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self._diskmounts = []
        self._diskusages = []
        self._diskusagefmts = []
        for part in psutil.disk_partitions():
            self._diskmounts.append(part.mountpoint)
            self._diskusages.append(tk.IntVar())
            self._diskusagefmts.append(tk.StringVar())
        self.frame = ttk.Frame(self)
        self.frame.grid()
        base_font = font.nametofont("TkDefaultFont")
        large_font = _common.modify_named_font(
            "TkDefaultFont", size=base_font.actual()["size"]+4
        )
        fixed_font = font.nametofont("TkFixedFont")
        ttk.Label(
            self.frame, text=_("Disk Usage"), font=large_font
        ).grid(columnspan=2)
        self._disklabels = []
        for col, mountpoint in enumerate(self._diskmounts):
            ttk.Label(
                self.frame, text=mountpoint, anchor=tk.SW,
                font=base_font
            ).grid(row=2*col + 1, column=0, sticky=tk.W)
            ttk.Progressbar(
                self.frame, length=300, orient=tk.HORIZONTAL, variable=self._diskusages[col]
            ).grid(row=2*col + 2, column=0)
            usagelabel = ttk.Label(
                self.frame, textvariable=self._diskusagefmts[col], anchor=tk.E,
                font=fixed_font
            )
            self._disklabels.append(usagelabel)
            usagelabel.grid(
                row=2*col + 2, column=1, padx=_common.INTERNAL_PAD, sticky=tk.E
            )
        ttk.Button(
            self.frame, text=_("Close"), command=self.dismiss,
            style='Accent.TButton'
        ).grid(
            row=2*len(self._diskmounts) + 2, column=1, sticky=tk.E,
            pady=_common.INTERNAL_PAD, padx=_common.INTERNAL_PAD
        )

    def reset(self):
        """
        Reset the dialog.
        """
        self.frame.destroy()
        self.create_widgets()
        self.update_screen()

    def update_screen(self):
        """
        Update the modal dialog window.
        """
        # update the mount points
        for part in psutil.disk_partitions():
            if part.mountpoint not in self._diskmounts:
                # newly mounted drive discovered - reset the widget
                self.reset()
                return
        # process the mount points
        for col, mountpoint in enumerate(self._diskmounts):
            try:
                usage = psutil.disk_usage(mountpoint).percent
                self._diskusages[col].set(round(usage))
                self._diskusagefmts[col].set(_common.disk_usage(mountpoint))
                if usage >= _common.DISK_ALERT_LEVEL:
                    style_name = "Alert.TLabel"
                elif usage >= _common.DISK_WARN_LEVEL:
                    style_name = "Warn.TLabel"
                else:
                    style_name = "Safe.TLabel"
                self._disklabels[col].configure(style=style_name)
            except FileNotFoundError:
                # disk was unmounted, reset the widget
                self.reset()
                return
        self.after(_common.REFRESH_INTERVAL, self.update_screen)


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
        self, settings: Settings, parent=None, title: Optional[str] = None,
        iconpath: Optional[str] = None
    ):
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
        super().__init__(parent, title=title, iconpath=iconpath)

    def update_screen(self):
        """
        Update the modal dialog window.

        This dialog does not require screen updates.
        """

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.
        """
        self.style.configure(
            "Switch.TCheckbutton", font=font.nametofont("TkDefaultFont")
        )

    def create_widgets(self) -> None:
        """
        Create the widgets to be displayed in the modal dialog.
        """
        self.always_on_top = tk.IntVar()
        self.always_on_top.set(self.settings.get_always_on_top())
        self.fonts = {
            "regular": self.settings.regular_font.get_full_font().get_string(),
            "fixed": self.settings.fixed_font.get_full_font().get_string()
        }
        frame = ttk.Frame(self, padding=_common.INTERNAL_PAD)
        frame.grid()
        base_font = font.nametofont("TkDefaultFont")
        self.parent.option_add('*TCombobox*Listbox.font', base_font)
        ttk.Label(
            frame, text=_("Language"), font=base_font
        ).grid(row=1, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.langbox = DropDown(
            frame, dictionary=LANGUAGES, state=["readonly"], exportselection=0,
            font=base_font
        )
        self.langbox.set(self.settings.get_language())
        self.langbox.grid(row=1, column=2, pady=_common.INTERNAL_PAD)
        self.langbox.bind("<<ComboboxSelected>>", self.change_combobox)
        ttk.Label(
            frame, text=_("Theme"), font=base_font
        ).grid(row=2, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        # Language translation is used as keys, and English is used as values
        # so that English is stored in the settings file, while allowing the
        # user to choose their theme based on their selected language.
        themes = {
            _("Light"): "Light",
            _("Dark"): "Dark",
            _("Same as System"): "Same as System"
        }
        self.themebox = DropDown(
            frame, dictionary=themes, state=["readonly"], exportselection=0,
            font=base_font
        )
        self.themebox.set(self.settings.get_theme())
        self.themebox.grid(row=2, column=2, pady=_common.INTERNAL_PAD)
        self.themebox.bind("<<ComboboxSelected>>", self.change_combobox)
        ttk.Checkbutton(
            frame, text=_("Always on top"), variable=self.always_on_top,
            style='Switch.TCheckbutton'
        ).grid(
            row=3, column=2,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        ttk.Label(
            frame, text=_("Regular Font"), font=base_font
        ).grid(row=4, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.font_button = ttk.Button(
            frame, text=self.fonts["regular"], command=self.show_font_chooser
        )
        self.font_button.grid(
            row=4, column=2,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        ttk.Label(
            frame, text=_("Monospace Font"), font=base_font
        ).grid(row=5, column=1, sticky=tk.E, padx=_common.INTERNAL_PAD)
        self.fixed_font_button = ttk.Button(
            frame, text=self.fonts["fixed"], command=self.show_fixedfont_chooser
        )
        self.fixed_font_button.grid(
            row=5, column=2,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        buttonframe = ttk.Frame(frame)
        ttk.Button(
            buttonframe, text=_("Cancel"), command=self.dismiss
        ).grid(row=1, column=1, padx=_common.INTERNAL_PAD/2)
        ttk.Button(
            buttonframe, text=_("OK"), command=self.save_and_dismiss,
            style='Accent.TButton'
        ).grid(row=1, column=2, padx=_common.INTERNAL_PAD/2)
        buttonframe.grid(row=6, column=1, columnspan=3, sticky=tk.E)

    def change_combobox(self, event: tk.Event):
        """
        Clear the selection when an item is selected in the combobox.
        """
        event.widget.selection_clear()

    def show_font_chooser(self, *_args):
        """
        Show a font chooser dialog.
        """
        chooser = FontChooser(
            self.parent, self.settings.regular_font.get_full_font(), self.iconpath
        )
        chosen_font = chooser.get_font()
        self.settings.regular_font.set_full_font(chosen_font)
        self.font_button.config(
            text=self.settings.regular_font.get_full_font().get_string()
        )

    def show_fixedfont_chooser(self, *_args):
        """
        Show a font chooser dialog.
        """
        chooser = FontChooser(
            self.parent, self.settings.fixed_font.get_full_font(), self.iconpath
        )
        chosen_font = chooser.get_font()
        self.settings.fixed_font.set_full_font(chosen_font)
        self.fixed_font_button.config(
            text=self.settings.fixed_font.get_full_font().get_string()
        )

    def on_save(self, *_args):
        """
        Save the entered settings.
        """
        old_language = self.settings.get_language()
        self.settings.set_language(self.langbox.get())
        self.settings.set_theme(self.themebox.get())
        self.settings.set_always_on_top(self.always_on_top.get())
        self.settings.write_settings()
        if old_language != self.langbox.get():
            self.parent.event_generate("<<LanguageChanged>>")
        if (
            self.fonts["regular"] != self.settings.regular_font.get_full_font().get_string()
        ):
            self.parent.event_generate("<<FontChanged>>")
        if (
            self.fonts["fixed"] != self.settings.fixed_font.get_full_font().get_string()
        ):
            self.parent.event_generate("<<FontChanged>>")
        self.parent.event_generate("<<SettingsChanged>>")


class FontChooser(ModalDialog):  # pylint: disable=too-many-instance-attributes
    """
    Font chooser dialog.

    Attributes
    ----------
    current_font : FontDescription, optional
        The currently selected font.
    fontchoices : List[str]
        A list of font families available on the system.
    fontname : str
        The font name.
    fontsize : IntVar
        The font size.
    fontstyle : StringVar
        The font style.
    underline : BooleanVar
        A flag indicating whether the font uses underline.
    overstrike : BooleanVar
        A flag indicating whether the font uses strikethrough.
    preview_font : Font
        A font using the currently selected details. Used to show the user
        what a sample text looks like.
    """
    def __init__(self, parent, current_font: Optional[FontDescription] = None, iconpath=None):
        """
        Construct a FontChooser dialog.

        Parameters
        ----------
        parent : Misc, optional
            The parent widget.
        current_font : FontDescription, optional
            The currently selected font.
        iconpath : str
            The path to the icon to display in the window title bar.
        """
        title = _("Choose Font")
        self.current_font = current_font
        self.fontchoices = list(set(font.families()))
        self.fontchoices.sort()
        self.fontname = current_font.family if current_font is not None else None
        self.fontsize = tk.IntVar()
        self.fontsize.set(current_font.size if current_font is not None else 12)
        self.fontsize.trace_add("write", self._update_preview)
        self.fontstyle = tk.StringVar()
        if current_font is not None:
            self.fontstyle.set(current_font.get_style())
        else:
            self.fontstyle.set(FontDescription.REGULAR)  # default to regular
        self.fontstyle.trace_add("write", self._update_preview)
        self.underline = tk.BooleanVar()
        self.underline.set(current_font.underline if current_font is not None else False)
        self.underline.trace_add("write", self._update_preview)
        self.overstrike = tk.BooleanVar()
        self.overstrike.set(current_font.overstrike if current_font is not None else False)
        self.overstrike.trace_add("write", self._update_preview)
        super().__init__(parent, title, iconpath, class_="FontChooser")

    def init_styles(self):
        """
        Initialize the styles used in the modal dialog.
        """
        self.preview_font = Font(self, self.current_font.get_font())
        self.preview_text = "AaáBbḅCcçÑñXxẍYyýZzẑ 0123456789"

    def update_screen(self):
        """
        Update the modal dialog window.

        This dialog does not require screen updates.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets that are displayed in the dialog.
        """
        content = ttk.Frame(self, padding=_common.INTERNAL_PAD)
        content.grid()
        base_font = font.nametofont("TkDefaultFont")

        familyframe = ttk.Frame(content)
        familyframe.grid(
            row=0, rowspan=2, sticky=tk.N+tk.W,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        ttk.Label(
            familyframe, text=_("Font"), font=base_font
        ).grid(row=0, sticky=tk.W)
        choicesvar = tk.StringVar(value=self.fontchoices)  # type: ignore
        lbox = tk.Listbox(
            familyframe, listvariable=choicesvar, height=10, width=30, bd=1,
            exportselection=0, relief=tk.FLAT, background="#555555",
            font=base_font
        )
        if content.tk.call("ttk::style", "theme", "use") == "azure-dark":
            bg1 = "#333333"
            bg2 = "#444444"
        else:  # light theme
            bg1 = "#ffffff"
            bg2 = "#eeeeff"
        for idx, item in enumerate(self.fontchoices):
            lbox.itemconfig(idx, {'bg': bg1 if idx % 2 else bg2})
            if item == self.fontname:
                lbox.selection_set(idx)
                lbox.see(idx)
        lbox.grid(row=1, column=0)
        scroll = ttk.Scrollbar(familyframe, orient=tk.VERTICAL)
        scroll.grid(row=1, column=1, sticky=tk.N+tk.S)
        lbox.config(yscrollcommand=scroll.set)
        scroll.config(command=lbox.yview)
        lbox.bind("<<ListboxSelect>>", self._on_select)

        styleframe = ttk.LabelFrame(
            content, labelwidget=ttk.Label(content, text=_("Style"), font=base_font)
        )
        styleframe.grid(
            row=0, column=1, sticky=tk.N+tk.W+tk.E,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        ttk.Radiobutton(
            styleframe, text=_("Regular"), value=FontDescription.REGULAR,
            variable=self.fontstyle
        ).grid(row=1, padx=_common.INTERNAL_PAD, sticky=tk.N+tk.S+tk.W+tk.E)
        ttk.Radiobutton(
            styleframe, text=_("Bold"), value=FontDescription.BOLD,
            variable=self.fontstyle
        ).grid(row=2, padx=_common.INTERNAL_PAD, sticky=tk.N+tk.S+tk.W+tk.E)
        ttk.Radiobutton(
            styleframe, text=_("Italic"), value=FontDescription.ITALIC,
            variable=self.fontstyle
        ).grid(row=3, padx=_common.INTERNAL_PAD, sticky=tk.N+tk.S+tk.W+tk.E)
        ttk.Radiobutton(
            styleframe, text=_("Bold Italic"), value=FontDescription.BOLD_ITALIC,
            variable=self.fontstyle
        ).grid(row=4, padx=_common.INTERNAL_PAD, sticky=tk.N+tk.S+tk.W+tk.E)

        effectsframe = ttk.LabelFrame(
            content, labelwidget=ttk.Label(content, text=_("Effects"), font=base_font)
        )
        effectsframe.grid(
            row=1, column=1, sticky=tk.N+tk.W+tk.E,
            padx=_common.INTERNAL_PAD
        )
        ttk.Checkbutton(
            effectsframe, text=_("Underline"), variable=self.underline,
            style='Switch.TCheckbutton'
        ).grid(row=0, column=0, padx=_common.INTERNAL_PAD, sticky=tk.W)
        ttk.Checkbutton(
            effectsframe, text=_("Overstrike"), variable=self.overstrike,
            style='Switch.TCheckbutton'
        ).grid(row=1, column=0, padx=_common.INTERNAL_PAD, sticky=tk.W)

        ScaleSpinner(
            content, self.fontsize, text=_("Size"), length=71*4, from_=1, to=72,
            as_int=True
        ).grid(row=2, columnspan=2)

        previewframe = ttk.LabelFrame(
            content,
            labelwidget=ttk.Label(content, text=_("Preview"), font=base_font)
        )
        previewframe.grid(
            row=3, columnspan=2, sticky=tk.N+tk.S+tk.W+tk.E,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        # Specifically using tk.Label here to convert the width to pixels when
        # an image is included - ttk.Label does not have this same "feature".
        # This fixes the width, not allowing the label to change size when the
        # font size changes.
        tk.Label(
            previewframe, text=self.preview_text, font=self.preview_font,
            image=tk.PhotoImage(width=1, height=1), width=420,
            compound=tk.CENTER, anchor=tk.SW
        ).grid(sticky=tk.N+tk.S+tk.W+tk.E, padx=_common.INTERNAL_PAD)

        buttonframe = ttk.Frame(content)
        buttonframe.grid(row=4, columnspan=2, sticky=tk.E)
        ttk.Button(
            buttonframe, text=_("Cancel"), command=self.dismiss
        ).grid(row=0, column=1, padx=_common.INTERNAL_PAD/2)
        ttk.Button(
            buttonframe, text=_("OK"), command=self.save_and_dismiss,
            style='Accent.TButton'
        ).grid(row=0, column=2, padx=_common.INTERNAL_PAD/2)

    def _update_preview(self, *_args):
        self.preview_font.configure(
            family=self.fontname,
            size=self.fontsize.get(),
            weight="bold" if self.fontstyle.get() in ['b', 'bi'] else "normal",
            slant="italic" if self.fontstyle.get() in ['i', 'bi'] else "roman",
            underline=self.underline.get(),
            overstrike=self.overstrike.get()
        )

    def _on_select(self, event: Event):
        widget: tk.Listbox = event.widget
        value = widget.get(widget.curselection()[0])
        self.fontname = value
        self._update_preview()

    def on_save(self) -> None:
        """
        Update `current_font` based on currently selected options.
        """
        weight: Literal['bold', 'normal'] = "normal"
        slant: Literal['italic', 'roman'] = "roman"
        if self.fontstyle.get() == FontDescription.BOLD:
            weight = "bold"
        elif self.fontstyle.get() == FontDescription.ITALIC:
            slant = "italic"
        elif self.fontstyle.get() == FontDescription.BOLD_ITALIC:
            weight = "bold"
            slant = "italic"
        self.current_font = FontDescription(
            family=self.fontname,
            size=self.fontsize.get(),
            weight=weight,
            slant=slant,
            underline=self.underline.get(),
            overstrike=self.overstrike.get()
        ) if self.fontname is not None else None

    def get_font(self) -> Optional[FontDescription]:
        """
        Get the full font specification based on user's choices.
        """
        return self.current_font
