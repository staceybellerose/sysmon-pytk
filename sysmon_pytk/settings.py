# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Application settings.
"""

from __future__ import annotations

from configparser import ConfigParser
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from .font_utils import MAIN_FONT_FAMILY, FontDescription

if TYPE_CHECKING:
    from tkinter.font import Font


class FontSettings:  # pylint: disable=too-many-instance-attributes
    """
    Manage the fonts used in the application.

    Attributes
    ----------
    config : ConfigParser
        A configuration file parser.
    section : str
        Which section of the configuration file to use.
    """

    def __init__(self, config: ConfigParser, section: str) -> None:
        self.config = config
        self.section = section

    @property
    def name(self) -> str:
        """
        The font name to use in the application.
        """
        return self.config[self.section].get("name", fallback=MAIN_FONT_FAMILY)

    @name.setter
    def name(self, fontname: str) -> None:
        self.config[self.section]["name"] = fontname

    @property
    def size(self) -> int:
        """
        The font size to use in the application.
        """
        return self.config[self.section].getint("size", fallback=12)

    @size.setter
    def size(self, fontsize: int) -> None:
        self.config[self.section]["size"] = f"{fontsize}"

    @property
    def weight(self) -> Literal["bold", "normal"]:
        """
        The font weight to use in the application.
        """
        weight = self.config[self.section].get("weight", fallback="normal")
        if weight == "bold":
            return "bold"
        return "normal"

    @weight.setter
    def weight(self, weight: str) -> None:
        self.config[self.section]["weight"] = weight

    @property
    def slant(self) -> Literal["italic", "roman"]:
        """
        The font slant to use in the application.
        """
        slant = self.config[self.section].get("slant", fallback="roman")
        if slant == "italic":
            return "italic"
        return "roman"

    @slant.setter
    def slant(self, slant: str) -> None:
        self.config[self.section]["slant"] = slant

    @property
    def underline(self) -> bool:
        """
        The font underline flag to use in the application.
        """
        return self.config[self.section].getboolean("underline", fallback=False)

    @underline.setter
    def underline(self, underline: bool) -> None:
        self.config[self.section]["underline"] = f"{underline}"

    @property
    def overstrike(self) -> bool:
        """
        The font overstrike flag to use in the application.
        """
        return self.config[self.section].getboolean("overstrike", fallback=False)

    @overstrike.setter
    def overstrike(self, overstrike: bool) -> None:
        self.config[self.section]["overstrike"] = f"{overstrike}"

    def get_full_font(self) -> FontDescription:
        """
        Get the full font specification to use in the application.
        """
        return FontDescription(
            family=self.name,
            size=self.size,
            weight=self.weight,
            slant=self.slant,
            underline=self.underline,
            overstrike=self.overstrike
        )

    def set_full_font(self, font: FontDescription) -> None:
        """
        Set the full font specification to use in the application.
        """
        self.name = font.family
        self.size = font.size
        self.weight = font.weight
        self.slant = font.slant
        self.underline = font.underline
        self.overstrike = font.overstrike

    def configure_font(self, font: Font) -> None:
        """
        Configure an existing Font to use the current settings.
        """
        font.configure(
            family=self.name,
            size=self.size,
            weight=self.weight,
            slant=self.slant,
            underline=self.underline,
            overstrike=self.overstrike
        )


class Settings:
    """
    Manage the application settings.

    Attributes
    ----------
    filename : str
        The full path to the configuration file.
    config : ConfigParser
        A configuration file parser.
    regular_font : FontSettings
        Font settings for the regular font.
    fixed_font : FontSettings
        Font settings for the monospace font.
    """

    def __init__(self, settings_file: str) -> None:
        self.filename = settings_file
        self.config = ConfigParser()
        self.read_settings()
        self.regular_font = FontSettings(self.config, "font")
        self.fixed_font = FontSettings(self.config, "fixedfont")

    def read_settings(self) -> None:
        """
        Read the settings from the configuration file.
        """
        self.config.read(self.filename)
        if not self.config.has_section("general"):
            self.config.add_section("general")
        if not self.config.has_section("font"):
            self.config.add_section("font")
        if not self.config.has_section("fixedfont"):
            self.config.add_section("fixedfont")

    def write_settings(self) -> None:
        """
        Write the settings to the configuration file.
        """
        with Path(self.filename).open(mode="w", encoding="utf-8") as file:
            self.config.write(file)

    @property
    def theme(self) -> str:
        """
        The application theme.
        """
        return self.config["general"].get("theme", fallback="Light")

    @theme.setter
    def theme(self, theme: str) -> None:
        self.config["general"]["theme"] = theme

    @property
    def always_on_top(self) -> int:
        """
        The flag indicating whether the application should always be on top.
        """
        return self.config["general"].getint("always_on_top", fallback=0)

    @always_on_top.setter
    def always_on_top(self, always_on_top: int) -> None:
        self.config["general"]["always_on_top"] = f"{always_on_top}"

    @property
    def add_menu_icon(self) -> int:
        """
        The flag indicating whether the application should add a menu icon.
        """
        return self.config["general"].getint("add_menu_icon", fallback=0)

    @add_menu_icon.setter
    def add_menu_icon(self, add_menu_icon: int) -> None:
        self.config["general"]["add_menu_icon"] = f"{add_menu_icon}"

    @property
    def language(self) -> str:
        """
        The language to use.
        """
        return self.config["general"].get("language", fallback="en")

    @language.setter
    def language(self, language: str) -> None:
        self.config["general"]["language"] = language
