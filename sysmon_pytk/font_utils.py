# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Font utilities.
"""

import dataclasses
from typing import Literal, Optional, TypeVar
from tkinter import font
from tkinter.font import Font

from .app_locale import _

MAIN_FONT_FAMILY = "Source Sans Pro"
FIXED_FONT_FAMILY = "Source Code Pro"

T = TypeVar("T")


@dataclasses.dataclass
class FontDescription():
    """
    Font data, like what is returned by the `actual` method of a `Font` object.

    Attributes
    ----------
    family : str
        The font family name.
    size : int
        The font size.
    weight : {'bold', 'normal'}
        The font weight.
    slant : {'italic', 'roman'}
        The font slant.
    underline : bool
        Whether the font uses underline.
    overstrike : bool
        Whether the font uses strikethrough.
    """

    family: str
    size: int
    weight: Literal['bold', 'normal']
    slant: Literal['italic', 'roman']
    underline: bool
    overstrike: bool

    REGULAR = 'r'
    BOLD = 'b'
    ITALIC = 'i'
    BOLD_ITALIC = 'bi'

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
        if style == FontDescription.BOLD:
            style_text = _("Bold")
        elif style == FontDescription.ITALIC:
            style_text = _("Italic")
        elif style == FontDescription.BOLD_ITALIC:
            style_text = _("Bold Italic")
        return f"{self.family} {style_text} {self.size}"

    def get_style(self) -> str:
        """
        Get the font style, based on its slant and weight.
        """
        if self.weight == 'bold' and self.slant == 'roman':
            return FontDescription.BOLD
        if self.weight == 'normal' and self.slant == 'italic':
            return FontDescription.ITALIC
        if self.weight == 'bold' and self.slant == 'italic':
            return FontDescription.BOLD_ITALIC
        return FontDescription.REGULAR


def modify_named_font(  # pylint: disable=too-many-arguments
    font_name: str, *,
    size: Optional[int] = None,
    weight: Optional[Literal['normal', 'bold']] = None,
    slant: Optional[Literal['roman', 'italic']] = None,
    underline: Optional[bool] = None,
    overstrike: Optional[bool] = None
) -> Font:
    """
    Modify a named font by optionally changing weight, size, slant, etc.

    Parameters
    ----------
    font_name : str
        The name of the font to use
    size : int, optional
        The font size to use
    weight : Literal['normal', 'bold'], optional
        The font weight to use
    slant : Literal['roman', 'italic'], optional
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
            family=fnt['family'],
            size=get_with_fallback(size, fnt['size']),
            weight=get_with_fallback(weight, fnt['weight']),
            slant=get_with_fallback(slant, fnt['slant']),
            underline=get_with_fallback(underline, fnt['underline']),
            overstrike=get_with_fallback(overstrike, fnt['overstrike'])
        )
    return Font(name="TkDefaultFont")


def get_with_fallback(value: Optional[T], fallback: T) -> T:
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
