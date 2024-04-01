# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Application font settings modal dialog.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import font, ttk
from typing import TYPE_CHECKING, Literal

from .. import _common
from ..app_locale import get_translator
from ..settings import FontDescription
from ..style_manager import StyleManager
from ..widgets import ScaleSpinner
from ._base_modal import ModalDialog

if TYPE_CHECKING:
    from tkinter import Event, Listbox, Misc

_ = get_translator()

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-instance-attributes


class FontChooser(ModalDialog):
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

    PREVIEW_TEXT = "AaÁáÅåCcÇçNnÑñSsẞßUuÜü 0123456789"

    def __init__(
        self, parent: Misc | None = None, *,
        current_font: FontDescription | None = None,
        iconpath: str | None = None
    ) -> None:
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
        self.fontsize = tk.IntVar()
        self.fontstyle = tk.StringVar()
        self.underline = tk.BooleanVar()
        self.overstrike = tk.BooleanVar()
        if self.current_font is not None:
            self.fontname: str | None = self.current_font.family
            self.fontstyle.set(self.current_font.get_style())
            self.fontsize.set(self.current_font.size)
            self.underline.set(self.current_font.underline)
            self.overstrike.set(self.current_font.overstrike)
            self.preview_font = self.current_font.get_font()
        else:
            # default selections
            self.fontname = None
            self.fontstyle.set(FontDescription.REGULAR)
            self.fontsize.set(12)
            self.underline.set(False)
            self.overstrike.set(False)
            self.preview_font = self.base_font
        self.fontsize.trace_add("write", self._update_preview)
        self.fontstyle.trace_add("write", self._update_preview)
        self.underline.trace_add("write", self._update_preview)
        self.overstrike.trace_add("write", self._update_preview)
        super().__init__(parent, title=title, iconpath=iconpath, class_="FontChooser")

    def update_screen(self) -> None:
        """
        Update the modal dialog window.

        This dialog does not require screen updates.
        """

    def create_widgets(self) -> None:
        """
        Create the widgets that are displayed in the dialog.
        """
        self.internal_frame.rowconfigure(1, weight=1)
        self.internal_frame.columnconfigure(0, weight=1)
        self._create_font_family_widget_frame()
        self._create_font_option_widgets()
        self._create_font_size_widgets()
        self._create_font_preview_widgets()
        self.add_ok_cancel_buttons()
        self.add_sizegrip()

    def _create_font_family_widget_frame(self) -> None:
        familyframe = ttk.Frame(self.internal_frame)
        familyframe.grid(
            row=0, rowspan=2, sticky=tk.NSEW,
            padx=(_common.INTERNAL_PAD, 0), pady=(_common.INTERNAL_PAD, 0)
        )
        familyframe.rowconfigure(1, weight=1)
        familyframe.columnconfigure(0, weight=1)
        ttk.Label(
            familyframe, text=_("Font"), font=self.base_font
        ).grid(row=0, sticky=tk.NSEW)
        choicesvar = tk.StringVar(value=self.fontchoices)  # type: ignore[arg-type]
        lbox = tk.Listbox(
            familyframe, listvariable=choicesvar, height=10, width=30, bd=1,
            exportselection=0, relief=tk.FLAT, background="#555555",
            font=self.base_font
        )
        bg1 = StyleManager.test_dark_mode("#333333", "#ffffff")
        bg2 = StyleManager.test_dark_mode("#444444", "#eeeeff")
        for idx, item in enumerate(self.fontchoices):
            item_bg = bg1 if idx % 2 else bg2
            lbox.itemconfig(idx, background=item_bg)
            if item == self.fontname:
                lbox.selection_set(idx)
                lbox.see(idx)
        lbox.grid(row=1, column=0, sticky=tk.NSEW)
        scroll = ttk.Scrollbar(familyframe, orient=tk.VERTICAL)
        scroll.grid(row=1, column=1, sticky=tk.NS)
        lbox.config(yscrollcommand=scroll.set)
        scroll.config(command=lbox.yview)
        lbox.bind("<<ListboxSelect>>", self._on_select)

    def _create_font_option_widgets(self) -> None:
        styleframe = ttk.LabelFrame(
            self.internal_frame,
            labelwidget=ttk.Label(
                self.internal_frame, text=_("Style"), font=self.base_font
            )
        )
        styleframe.grid(
            row=0, column=1, sticky=tk.NSEW,
            padx=_common.INTERNAL_PAD, pady=_common.INTERNAL_PAD
        )
        ttk.Radiobutton(
            styleframe, text=_("Regular"), value=FontDescription.REGULAR,
            variable=self.fontstyle
        ).grid(row=1, padx=_common.INTERNAL_PAD, sticky=tk.NSEW)
        ttk.Radiobutton(
            styleframe, text=_("Bold"), value=FontDescription.BOLD,
            variable=self.fontstyle
        ).grid(row=2, padx=_common.INTERNAL_PAD, sticky=tk.NSEW)
        ttk.Radiobutton(
            styleframe, text=_("Italic"), value=FontDescription.ITALIC,
            variable=self.fontstyle
        ).grid(row=3, padx=_common.INTERNAL_PAD, sticky=tk.NSEW)
        ttk.Radiobutton(
            styleframe, text=_("Bold Italic"), value=FontDescription.BOLD_ITALIC,
            variable=self.fontstyle
        ).grid(row=4, padx=_common.INTERNAL_PAD, sticky=tk.NSEW)

        effectsframe = ttk.LabelFrame(
            self.internal_frame,
            labelwidget=ttk.Label(
                self.internal_frame, text=_("Effects"), font=self.base_font
            )
        )
        effectsframe.grid(
            row=1, column=1, sticky=tk.N, padx=_common.INTERNAL_PAD
        )
        ttk.Checkbutton(
            effectsframe, text=_("Underline"), variable=self.underline,
            style="Switch.TCheckbutton"
        ).grid(row=0, column=0, padx=_common.INTERNAL_PAD, sticky=tk.W)
        ttk.Checkbutton(
            effectsframe, text=_("Overstrike"), variable=self.overstrike,
            style="Switch.TCheckbutton"
        ).grid(row=1, column=0, padx=_common.INTERNAL_PAD, sticky=tk.W)

    def _create_font_size_widgets(self) -> None:
        ScaleSpinner(
            self.internal_frame, self.fontsize, text=_("Size"), length=71*4,
            from_=1, to=72, as_int=True
        ).grid(
            row=2, columnspan=2, sticky=tk.NSEW, padx=_common.INTERNAL_PAD,
            pady=(_common.INTERNAL_PAD, 0)
        )

    def _create_font_preview_widgets(self) -> None:
        previewframe = ttk.LabelFrame(
            self.internal_frame, height=150, width=500,
            labelwidget=ttk.Label(
                self.internal_frame, text=_("Preview"), font=self.base_font
            )
        )
        previewframe.grid(
            row=3, columnspan=2, sticky=tk.NSEW,
            padx=_common.INTERNAL_PAD, pady=(0, _common.INTERNAL_PAD)
        )
        previewframe.columnconfigure(0, weight=1)
        previewframe.rowconfigure(0, weight=1)
        previewframe.grid_propagate(False)
        ttk.Label(
            previewframe, text=self.PREVIEW_TEXT, font=self.preview_font,
            anchor=tk.CENTER
        ).grid(sticky=tk.NSEW)

    def _update_preview(self, *_args) -> None:
        if self.fontname:
            self.preview_font.configure(
                family=self.fontname,
                size=self.fontsize.get(),
                weight="bold" if self.fontstyle.get() in {"b", "bi"} else "normal",
                slant="italic" if self.fontstyle.get() in {"i", "bi"} else "roman",
                underline=self.underline.get(),
                overstrike=self.overstrike.get()
            )

    def _on_select(self, event: Event[Listbox]) -> None:
        value = event.widget.get(event.widget.curselection()[0])
        self.fontname = value
        self._update_preview()

    def on_save(self) -> None:
        """
        Update `current_font` based on currently selected options.
        """
        weight: Literal["bold", "normal"] = "normal"
        slant: Literal["italic", "roman"] = "roman"
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

    def get_font(self) -> FontDescription | None:
        """
        Get the full font specification based on user's choices.
        """
        return self.current_font
