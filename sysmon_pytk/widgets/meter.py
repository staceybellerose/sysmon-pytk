# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Meter widget.
"""

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-locals

import dataclasses
import tkinter as tk
from tkinter import ttk

from .._common import is_dark
from ..font_utils import modify_named_font


class Meter(tk.Frame):
    """
    Shows a meter widget, like a speedometer.
    """

    GREEN = "#0a0"
    YELLOW = "#dd0"
    RED = "#d00"
    BLUE = "#00a"

    START_ANGLE = 36
    EXTENT_ANGLE = 180 - 2*START_ANGLE

    @dataclasses.dataclass
    class CanvasObjects:
        """
        Various canvas objects that need to be tracked.
        """

        label1: int = 0
        min_value: int = 0
        max_value: int = 0
        current: int = 0
        meter: int = 0
        inset: int = 0
        inset_border: int = 0
        wedges: list = dataclasses.field(default_factory=lambda: [])

    def __init__(
            self,
            parent, *,
            width: int = 300,
            height: int = 225,
            min_value: float = 0.0,
            max_value: float = 100.0,
            label: str = "",
            unit: str = "",
            divisions: int = 10,
            yellow: float = 15,
            red: float = 15,
            blue: float = 0, **kw
    ):
        self._unit = unit
        self._min_value = min_value
        self._max_value = max_value
        self.range = {"blue": blue, "yellow": yellow, "red": red}
        font_size_lg = int(height / 15)
        font_size_sm = int(height / 20)
        text_font = modify_named_font("TkDefaultFont", size=font_size_lg)
        large_font = modify_named_font("TkFixedFont", size=font_size_lg)
        small_font = modify_named_font("TkFixedFont", size=font_size_sm)
        self.check_dark_mode()
        super().__init__(parent, background=self._background, class_="Meter", **kw)
        self.var = tk.DoubleVar(self, 0)
        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            background=self._background,
            borderwidth=0,
            highlightthickness=0
        )
        self.canvas_objects = self.CanvasObjects()

        # Add text: label, mix, max, current
        self.canvas_objects.label1 = self.canvas.create_text(
            width / 2, height / 10,
            font=text_font, text=label, fill=self._text_color
        )
        self.canvas_objects.min_value = self.canvas.create_text(
            width / 6, height * 0.55,
            font=small_font, text=f"{int(self._min_value)}{unit}",
            fill=self._text_color, anchor=tk.NE, justify=tk.RIGHT
        )
        self.canvas_objects.max_value = self.canvas.create_text(
            width * 5 / 6, height * 0.55,
            font=small_font, text=f"{int(self._max_value)}{unit}",
            fill=self._text_color, anchor=tk.NW, justify=tk.LEFT
        )
        self.canvas_objects.current = self.canvas.create_text(
            width / 2, height - 1.75*font_size_lg,
            font=large_font, text=f"{self.var.get()}{self._unit}",
            fill=self._text_color, anchor=tk.N, justify=tk.CENTER
        )

        coord = width / 30, height / 4, width * 29 / 30, height * 1.5
        # Add the divisions
        self.canvas_objects.wedges = []
        for i in range(divisions):
            self.canvas_objects.wedges.append(self.canvas.create_arc(
                coord,
                start=(i * (Meter.EXTENT_ANGLE / divisions) + Meter.START_ANGLE),
                extent=(Meter.EXTENT_ANGLE / divisions),
                width=1, outline=self._text_color
            ))

        # Add the color scale arcs
        self.canvas.create_arc(
            coord,
            extent=Meter.EXTENT_ANGLE, start=Meter.START_ANGLE,
            style='arc', outline=self.GREEN, width=width / 12
        )
        if red > 0:
            self.canvas.create_arc(
                coord,
                extent=self._percent_to_degrees(red), start=Meter.START_ANGLE,
                style='arc', outline=self.RED, width=width / 12
            )
        if yellow > 0:
            self.canvas.create_arc(
                coord,
                extent=self._percent_to_degrees(yellow),
                start=self._percent_to_degrees(red) + Meter.START_ANGLE,
                style='arc', outline=self.YELLOW, width=width / 12
            )
        if blue > 0:
            self.canvas.create_arc(
                coord,
                start=Meter.EXTENT_ANGLE + Meter.START_ANGLE,
                extent=-self._percent_to_degrees(blue),
                style='arc', outline=self.BLUE, width=width / 12
            )

        # Add the moving indicator line
        self.canvas_objects.meter = self.canvas.create_arc(
            coord,
            start=Meter.EXTENT_ANGLE + Meter.START_ANGLE, extent=1,
            fill=self._meter_color, outline=self._meter_color, width=3
        )

        # Add the inset
        inset_coord = width * 23 / 60, height * 23 / 32, width * 37 / 60, height * 33 / 32
        self.canvas_objects.inset = self.canvas.create_arc(
            inset_coord,
            start=Meter.START_ANGLE, extent=Meter.EXTENT_ANGLE,
            fill=self._text_color, outline=self._text_color, width=2
        )
        self.canvas_objects.inset_border = self.canvas.create_arc(
            inset_coord,
            start=Meter.START_ANGLE, extent=Meter.EXTENT_ANGLE,
            outline=self._meter_color, style="arc", width=1
        )

        self._update_meter_line(Meter.EXTENT_ANGLE + Meter.START_ANGLE)
        self.var.trace_add('write', self._update_meter)
        self.canvas.grid()

    def check_dark_mode(self):
        """
        Detect whether using dark mode and adjust base colors.
        """
        style = ttk.Style()
        self._text_color = style.lookup("TLabel", "foreground")
        self._background = style.lookup("TLabel", "background")
        dark_mode = is_dark(f"{self._background}")
        self._meter_color = "#ccc" if dark_mode else "#666"
        self._meter_red = "#f22" if dark_mode else "#c00"
        self._meter_yellow = "#ff2" if dark_mode else "#cc0"
        self._meter_blue = "#22f" if dark_mode else "#00c"

    def update_for_dark_mode(self):
        """
        Update the meter colors based on detected dark mode.
        """
        self.check_dark_mode()
        self.canvas.itemconfig(self.canvas_objects.label1, fill=self._text_color)
        self.canvas.itemconfig(self.canvas_objects.min_value, fill=self._text_color)
        self.canvas.itemconfig(self.canvas_objects.max_value, fill=self._text_color)
        self.canvas.itemconfig(self.canvas_objects.current, fill=self._text_color)
        self.canvas.itemconfig(self.canvas_objects.meter, fill=self._meter_color)
        self.canvas.itemconfig(self.canvas_objects.meter, outline=self._meter_color)
        self.canvas.itemconfig(self.canvas_objects.inset, fill=self._text_color)
        self.canvas.itemconfig(self.canvas_objects.inset, outline=self._text_color)
        self.canvas.itemconfig(self.canvas_objects.inset_border, outline=self._text_color)
        for wedge in self.canvas_objects.wedges:
            self.canvas.itemconfig(wedge, outline=self._text_color)

    def _update_meter_line(self, angle):
        """
        Update the meter line indicator.
        """
        self.canvas.itemconfig(self.canvas_objects.meter, start=angle)
        self.canvas.itemconfig(self.canvas_objects.current, text=f"{self.var.get()}{self._unit}")

    def _update_meter(self, _name1, _name2, _op):
        """
        Update the meter display based on the updated variable.
        """
        pct = (self.var.get() - self._min_value)/(self._max_value - self._min_value)
        if pct * 100 < self.range["blue"]:
            self.canvas.itemconfig(self.canvas_objects.meter, fill=self._meter_blue)
            self.canvas.itemconfig(self.canvas_objects.meter, outline=self._meter_blue)
        elif pct * 100 > 100 - self.range["red"]:
            self.canvas.itemconfig(self.canvas_objects.meter, fill=self._meter_red)
            self.canvas.itemconfig(self.canvas_objects.meter, outline=self._meter_red)
        elif pct * 100 > 100 - self.range["red"] - self.range["yellow"]:
            self.canvas.itemconfig(self.canvas_objects.meter, fill=self._meter_yellow)
            self.canvas.itemconfig(self.canvas_objects.meter, outline=self._meter_yellow)
        else:
            self.canvas.itemconfig(self.canvas_objects.meter, fill=self._meter_color)
            self.canvas.itemconfig(self.canvas_objects.meter, outline=self._meter_color)
        angle = (1 - pct) * Meter.EXTENT_ANGLE + Meter.START_ANGLE
        self._update_meter_line(angle)

    def _percent_to_degrees(self, pct: float) -> float:
        return float(Meter.EXTENT_ANGLE) * pct / 100

    def set_value(self, value: float):
        """
        Set the value to display on the meter.
        """
        self.var.set(value)

    def bind(self, sequence=None, func=None, add=None):
        """
        Pass events through to the canvas, since frames don't normally respond to them.
        """
        return self.canvas.bind(sequence, func, add)
