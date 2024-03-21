# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Information about the app translators.
"""

from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Translator:
    """
    App translator data.
    """

    name: str
    github_username: str = ""

    def github_url(self) -> str:
        """
        Build the translator's github link from their username, if available.
        """
        if self.github_username is not None:
            return f"https://github.com/{self.github_username}"
        return None


TRANSLATORS: dict[str, list[Translator]] = {
    "Español": [
        Translator("Stacey Adams (author)")
    ],
    "Deutsch": [
        Translator("Alisyn Arness")
    ],
    "Norsk Bokmål": [
        Translator("Allan Nordhøy", "comradekingu")
    ]
}
