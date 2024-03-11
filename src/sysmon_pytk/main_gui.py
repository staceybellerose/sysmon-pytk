#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
System monitor.
"""

from .tkapplication import Application


def main_gui():
    """
    Entry point for GUI application.
    """
    app = Application()
    app.update()
    app.minsize(app.winfo_width(), app.winfo_height())
    app.mainloop()
