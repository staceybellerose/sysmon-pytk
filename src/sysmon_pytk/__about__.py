# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Metadata about the package.
"""

from .app_locale import _

__all__ = [
    "__app_name__", "__version__", "__author_name__", "__author_email__",
    "__author__", "__url__", "__keywords__", "__copyright_year__",
    "__license__", "__license_url__", "__summary__", "__full_license__"
]

__app_name__ = "sysmon-pytk"
__version__ = "0.3.0"
__author_name__ = "Stacey Adams"
__author_email__ = "stacey.belle.rose@gmail.com"
__author__ = f"{__author_name__} <{__author_email__}>"
__url__ = "https://github.com/staceybellerose/sysmon-pytk"
__keywords__ = "system monitor"
__copyright_year__ = "2024"
__license__ = _("MIT License")
__license_url__ = "https://opensource.org/licenses/MIT"
__summary__ = _("""\
sysmon-pytk is a system monitor. It monitors CPU usage and temperature, \
RAM usage, and disk usage of the primary disk (containing the root \
partition). It also displays the system's hostname, IP address, uptime, \
and current process count.""")
__full_license__ = """\
MIT License

Copyright © 2024 Stacey Adams

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
