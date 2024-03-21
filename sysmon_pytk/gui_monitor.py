#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
GUI System monitor.
"""

from .application import Application


def gui_monitor() -> None:
    """
    Entry point for GUI monitor.
    """
    app = Application()
    app.update()
    app.mainloop()


if __name__ == "__main__":
    gui_monitor()
