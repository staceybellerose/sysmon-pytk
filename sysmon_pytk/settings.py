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


class FontSettings:
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

    def get_name(self) -> str:
        """
        Get the font name to use in the application.
        """
        return self.config[self.section].get("name", fallback=MAIN_FONT_FAMILY)

    def set_name(self, fontname: str) -> None:
        """
        Set the font name to use in the application.
        """
        self.config[self.section]["name"] = fontname

    def get_size(self) -> int:
        """
        Get the font size to use in the application.
        """
        return self.config[self.section].getint("size", fallback=12)

    def set_size(self, fontsize: int) -> None:
        """
        Set the font size to use in the application.
        """
        self.config[self.section]["size"] = f"{fontsize}"

    def get_weight(self) -> Literal["bold", "normal"]:
        """
        Get the font weight to use in the application.
        """
        weight = self.config[self.section].get("weight", fallback="normal")
        if weight == "bold":
            return "bold"
        return "normal"

    def set_weight(self, weight: str) -> None:
        """
        Set the font weight to use in the application.
        """
        self.config[self.section]["weight"] = weight

    def get_slant(self) -> Literal["italic", "roman"]:
        """
        Get the font slant to use in the application.
        """
        slant = self.config[self.section].get("slant", fallback="roman")
        if slant == "italic":
            return "italic"
        return "roman"

    def set_slant(self, slant: str) -> None:
        """
        Set the font slant to use in the application.
        """
        self.config[self.section]["slant"] = slant

    def get_underline(self) -> bool:
        """
        Get the font underline flag to use in the application.
        """
        return self.config[self.section].getboolean("underline", fallback=False)

    def set_underline(self, underline: bool) -> None:  # noqa: FBT001
        """
        Set the font underline flag to use in the application.
        """
        self.config[self.section]["underline"] = f"{underline}"

    def get_overstrike(self) -> bool:
        """
        Get the font overstrike flag to use in the application.
        """
        return self.config[self.section].getboolean("overstrike", fallback=False)

    def set_overstrike(self, overstrike: bool) -> None:  # noqa: FBT001
        """
        Set the font overstrike flag to use in the application.
        """
        self.config[self.section]["overstrike"] = f"{overstrike}"

    def get_full_font(self) -> FontDescription:
        """
        Get the full font specification to use in the application.
        """
        return FontDescription(
            family=self.get_name(),
            size=self.get_size(),
            weight=self.get_weight(),
            slant=self.get_slant(),
            underline=self.get_underline(),
            overstrike=self.get_overstrike()
        )

    def set_full_font(self, font: FontDescription) -> None:
        """
        Set the full font specification to use in the application.
        """
        self.set_name(font.family)
        self.set_size(font.size)
        self.set_weight(font.weight)
        self.set_slant(font.slant)
        self.set_underline(font.underline)
        self.set_overstrike(font.overstrike)

    def configure_font(self, font: Font) -> None:
        """
        Configure an existing Font to use the current settings.
        """
        font.configure(
            family=self.get_name(),
            size=self.get_size(),
            weight=self.get_weight(),
            slant=self.get_slant(),
            underline=self.get_underline(),
            overstrike=self.get_overstrike()
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

    def get_theme(self) -> str:
        """
        Get the application theme.
        """
        return self.config["general"].get("theme", fallback="Light")

    def set_theme(self, theme: str) -> None:
        """
        Set the application theme.
        """
        self.config["general"]["theme"] = theme

    def get_always_on_top(self) -> int:
        """
        Get the flag indicating whether the application should always be on top.
        """
        return self.config["general"].getint("always_on_top", fallback=0)

    def set_always_on_top(self, always_on_top: int) -> None:
        """
        Set the flag indicating whether the application should always be on top.
        """
        self.config["general"]["always_on_top"] = f"{always_on_top}"

    def get_language(self) -> str:
        """
        Get the language to use.
        """
        return self.config["general"].get("language", fallback="en")

    def set_language(self, language: str) -> None:
        """
        Set the language to use.
        """
        self.config["general"]["language"] = language
