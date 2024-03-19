# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Dropdown widget.
"""

from tkinter import BaseWidget, ttk
from typing import Dict

# These lint errors don't make sense for GUI widgets, so are disabled here.
# pragma pylint: disable=too-many-ancestors


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
            parent, values=sorted(list(dictionary.keys())), *args, **kwargs
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
