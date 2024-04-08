# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Font utilities.
"""

from __future__ import annotations

import dataclasses
from enum import Enum
from tkinter import font
from tkinter.font import Font
from typing import Literal, TypeVar

from typing_extensions import Self, TypeAlias

from .app_locale import get_translator

_ = get_translator()

MAIN_FONT_FAMILY = "Source Sans Pro"
FIXED_FONT_FAMILY = "Source Code Pro"

T = TypeVar("T")

FontWeight: TypeAlias = Literal["normal", "bold"]
"""Font weight, one of `normal`, `bold`. For use with tk.Font."""

FontSlant: TypeAlias = Literal["roman", "italic"]
"""Font slant, one of `roman`, `italic`. For use with tk.Font."""


class FontStyle(Enum):
    """
    Font style.
    """

    REGULAR = "r"
    """Font style: Regular."""

    BOLD = "b"
    """Font style: Bold."""

    ITALIC = "i"
    """Font style: Italic."""

    BOLD_ITALIC = "bi"
    """Font style: Bold Italic."""

    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        for member in cls:
            if member.value == value:
                return member
        return None

    def is_bold(self) -> bool:
        """
        Determine whether the font style is bold.
        """
        return "b" in self.value

    def is_italic(self) -> bool:
        """
        Determine whether the font style is italc.
        """
        return "i" in self.value

    def get_weight(self) -> FontWeight:
        """
        Get the weight of the font style, either `normal` or `bold`.
        """
        return "bold" if self.is_bold() else "normal"

    def get_slant(self) -> FontSlant:
        """
        Get the slant of the font style, either `roman` or `italic`.
        """
        return "italic" if self.is_italic() else "roman"

    def to_weight_and_slant(self) -> tuple[FontWeight, FontSlant]:
        """
        Convert the font style to a weight and slant, for use with tk.Font.
        """
        weight: FontWeight = "normal"
        slant: FontSlant = "roman"
        if self == FontStyle.BOLD:
            weight = "bold"
        elif self == FontStyle.ITALIC:
            slant = "italic"
        elif self == FontStyle.BOLD_ITALIC:
            weight = "bold"
            slant = "italic"
        return (weight, slant)

    @classmethod
    def from_weight_and_slant(cls, weight: FontWeight, slant: FontSlant) -> FontStyle:
        """
        Given a weight and slant, return a FontStyle.

        Parameters
        ----------
        weight : FontWeight
            Font weight, one of `normal`, `bold`.
        slant : FontSlant
            Font slant, one of `roman`, `italic`.
        """
        if weight == "bold":
            if slant == "italic":
                return cls.BOLD_ITALIC
            return cls.BOLD
        if slant == "italic":
            return cls.ITALIC
        return cls.REGULAR


@dataclasses.dataclass
class FontDescription:
    """
    Font data, like what is returned by the `actual` method of a `Font` object.
    """

    family: str
    """The font family name."""
    size: int
    """The font size."""
    weight: FontWeight
    """The font weight."""
    slant: FontSlant
    """The font slant."""
    underline: bool
    """Whether the font uses underline."""
    overstrike: bool
    """Whether the font uses strikethrough."""

    def get_font(self) -> Font:
        """
        Return a Tk font based on this object's data.
        """
        return Font(
            family=self.family, size=self.size, weight=self.weight,
            slant=self.slant, underline=self.underline, overstrike=self.overstrike
        )

    def get_string(self) -> str:
        """
        Get the string which describes the font.
        """
        style = self.get_style()
        style_text = ""
        if style == FontStyle.BOLD:
            style_text = _("Bold")
        elif style == FontStyle.ITALIC:
            style_text = _("Italic")
        elif style == FontStyle.BOLD_ITALIC:
            style_text = _("Bold Italic")
        effects = self.get_effects()
        return " ".join(f"{self.family} {style_text} {effects} {self.size}".split())

    def get_style(self) -> FontStyle:
        """
        Get the font style, based on its slant and weight.
        """
        return FontStyle.from_weight_and_slant(self.weight, self.slant)

    def get_effects(self) -> str:
        """
        Get the font effects (underline/strikethrough).
        """
        underline = _("Underline") if self.underline else ""
        overstrike = _("Overstrike") if self.overstrike else ""
        return f"{underline} {overstrike}".strip()


def modify_named_font(  # pylint: disable=too-many-arguments
    font_name: str, *,
    size: int | None = None,
    weight: FontWeight | None = None,
    slant: FontSlant | None = None,
    underline: bool | None = None,
    overstrike: bool | None = None
) -> Font:
    """
    Modify a named font by optionally changing weight, size, slant, etc.

    Parameters
    ----------
    font_name : str
        The name of the font to use
    size : int, optional
        The font size to use
    weight : FontWeight, optional
        The font weight to use
    slant : FontSlant, optional
        The font slant to use
    underline : bool, optional
        Whether the font should be underlined
    overstrike : bool, optional
        Whether the font should have strikethrough

    Returns
    -------
    Font
        A new font, with the parameters given.

    Example
    -------
    >>> modify_named_font("TkDefaultFont", size=13, weight="bold").actual()
    {   'family': 'Bitstream Vera Sans',
        'size': 13,
        'weight': 'bold',
        'slant': 'roman',
        'underline': 0,
        'overstrike': 0 }
    """
    if font_name in font.names():
        fnt = font.nametofont(font_name).actual()
        return Font(
            family=fnt["family"],
            size=get_with_fallback(size, fnt["size"]),
            weight=get_with_fallback(weight, fnt["weight"]),
            slant=get_with_fallback(slant, fnt["slant"]),
            underline=get_with_fallback(underline, fnt["underline"]),
            overstrike=get_with_fallback(overstrike, fnt["overstrike"])
        )
    return Font(name="TkDefaultFont")


def get_with_fallback(value: T | None, fallback: T) -> T:
    """
    Return the value provided unless it is None. In that case, return the fallback.

    Parameters
    ----------
    value : Optional[T]
        Any value, possibly None
    fallback : T
        A fallback value, cannot be None

    Returns
    -------
    T
        A value that is not None
    """
    return value if value is not None else fallback
