# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Various Tk widgets.
"""

from typing import Any, Dict, Optional
import tkinter as tk
from tkinter import ttk, font, BaseWidget, Event, Variable
import webbrowser

import _common

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-arguments, too-many-ancestors


class ToolTip:
    """
    Display a hovering tooltip while the mouse is over a given widget.

    Attributes
    ----------
    tooltip : tk.Toplevel
        The actual tooltip popup.
    parent : BaseWidget
        The parent widget, which will host the tooltip.
    text : str
        The text to display in the tooltip.
    """

    def __init__(self, parent: BaseWidget, text: str = ''):
        """
        Construct a tooltip.

        Parameters
        ----------
        parent : BaseWidget
            The parent widget, which will host the tooltip.
        text : str
            The text to display in the tooltip.
        """
        self.tooltip: Optional[tk.Toplevel] = None
        self.parent = parent
        self.text = text
        self.parent.bind('<Enter>', self.on_enter)
        self.parent.bind('<Motion>', self.on_move)
        self.parent.bind('<Leave>', self.on_leave)

    def on_enter(self, event: Event):
        """
        Handle the event when pointer enters the widget.
        """
        self.tooltip = tk.Toplevel()
        self.tooltip.overrideredirect(True)
        self.tooltip.geometry(f'+{event.x_root+10}+{event.y_root+10}')
        ttk.Label(
            self.tooltip, text=self.text, anchor=tk.CENTER,
            background="#ffd", foreground="#000"
        ).grid(ipadx=_common.INTERNAL_PAD)

    def on_move(self, event: Event):
        """
        Handle the event when the pointer moves within the widget.
        """
        if self.tooltip:
            self.tooltip.geometry(f'+{event.x_root+10}+{event.y_root+10}')

    def on_leave(self, _event: Event):
        """
        Handle the event when the pointer leaves the widget.
        """
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class DropDown(ttk.Combobox):
    """
    A Combobox that takes a dict for values.

    Dict keys are used for display, and dict values are used for the
    value set or returned.

    Attributes
    ----------
    dictionary : dict
        The dictionary to use in the dropdown.
    """

    def __init__(self, parent: BaseWidget, dictionary: Dict, *args, **kwargs):
        """
        Construct a dropdown widget.

        Parameters
        ----------
        parent : BaseWidget
            The parent widget.
        dictionary : dict
            The dictionary to use in the dropdown.
        *args : tuple, optional
            Additional arguments for initializing a `Combobox`.
        **kwargs : dict, optional
            Additional keyword arguments for a `Combobox`.
        """
        super().__init__(
            parent, values=sorted(list(dictionary.keys())),
            *args, **kwargs
        )
        self.dictionary = dictionary

    def get(self) -> str:
        """
        Get the selected value.
        """
        key = super().get()
        return self.dictionary[key] if key != '' else ''

    def set(self, value: str):
        """
        Set the value of the dropdown, if value is found in the dictionary.
        """
        keys = [key for key, val in self.dictionary.items() if val == value]
        if len(keys) > 0:
            super().set(keys[0])


class UrlLabel(ttk.Label):
    """
    A label containing a clickable URL.

    Attributes
    ----------
    url : str
        The URL to use when opening a web browser.
    """

    def __init__(
        self, parent: BaseWidget, text: str, url: str,
        style: str = 'URL.TLabel', show_tooltip: bool = False, **kw
    ) -> None:
        """
        Construct a Label with a clickable URL.

        Parameters
        ----------
        parent : BaseWidget
            The parent widget.
        text : str
            The text to display in the label.
        url : str
            The URL to use when opening a web browser.
        style : str
            A Tcl/Tk style to use for display.
        show_tooltip : bool
            A flag to indicate whether to show a tooltip containing the URL.
        **kw : dict, optional
            Additional keyword arguments for a `Label`.
        """
        self.url = url
        cursor = 'hand2' if self._has_web_protocol() else 'arrow'
        super().__init__(parent, cursor=cursor, style=style, text=text, **kw)
        if show_tooltip and url:
            ToolTip(self, url)
        self.bind("<Button-1>", self.open_url)

    def open_url(self, _event: Event):
        """
        Open the widget's URL in a web browser.
        """
        if self._has_web_protocol():
            webbrowser.open_new_tab(self.url)

    def _has_web_protocol(self) -> bool:
        """
        Determine whether the string contains a web protocol (http or https).
        """
        return self.url[0:7] == 'http://' or self.url[0:8] == 'https://'

    @classmethod
    def has_web_protocol(cls, url: str) -> bool:
        """
        Determine whether the string contains a web protocol (http or https).
        """
        return url[0:7] == 'http://' or url[0:8] == 'https://'

    @classmethod
    def test_web_protocol(cls, url: str, trueval: Any, falseval: Any) -> Any:
        """
        If url uses a web protocol, return trueval; otherwise return falseval.
        """
        return trueval if cls.has_web_protocol(url) else falseval


class ScaleSpinner(ttk.Frame):
    """
    Combination of a Scale and Spinbox, with an optional Label.

    Attributes
    ----------
    variable : Variable
        The control variable which maintains the selected value.
    as_int : bool
        A flag indicating whether to round the values from the `Scale`.
    scale : Scale
        The `Scale` widget managed by this widget.
    spinbox : Spinbox
        The `Spinbox` widget managed by this widget.
    """

    def __init__(
            self, parent: BaseWidget, variable: Variable, *,
            text: Optional[str] = None, length: int = 100, from_: float = 0,
            to: float = 100, as_int: bool = False
    ):
        """
        Construct a frame containing a Scale, a Spinbox, and an optional Label.

        Parameters
        ----------
        parent : BaseWidget
            The parent widget.
        variable : Variable
            The control variable which maintains the selected value.
        text : str, optional
            The text to display as a `Label`.
        length : int, default: 100
            The length of the `Scale` widget.
        from_ : float, default: 0.0
            The smallest value allowed for the `Scale` and `Spinbox`.
        to : float, default: 100.0
            The largest value allowed for the `Scale` and `Spinbox`.
        as_int : bool, default: False
            A flag indicating whether to round the values from the `Scale`.
        """
        super().__init__(parent)
        self.variable = variable
        self.as_int = as_int
        base_font = font.nametofont("TkDefaultFont")
        if text is not None:
            ttk.Label(
                self, text=text, anchor=tk.W, font=base_font
            ).grid(row=0, column=0)
        self.scale = ttk.Scale(
            self, orient=tk.HORIZONTAL, length=length, from_=from_, to=to,
            style='Tick.TScale'
        )
        self.scale.grid(row=0, column=1, pady=10, padx=10)
        self.scale.set(variable.get())
        self.spinbox = ttk.Spinbox(
            self, textvariable=variable, from_=from_, to=to,
            width=len(f"{to}")+3, state='readonly', font=base_font,
            command=self.update_from_spinbox
        )
        self.spinbox.grid(row=0, column=2)
        self.scale.configure(command=self.update_from_scale)

    def update_from_spinbox(self):
        """
        Update font size from spinbox.
        """
        self.scale.set(self.variable.get())

    def update_from_scale(self, size):
        """
        Update font size from scale widget.
        """
        self.variable.set(round(float(size)) if self.as_int else float(size))
        self.spinbox.selection_clear()
