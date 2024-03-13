# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Shared functions used throughout the application.
"""

import os
import platform
import subprocess  # nosec B404
import re
import time
from socket import AF_INET
from typing import List, Literal, Union, Optional, TypeVar
from tkinter import font
from tkinter.font import Font

import psutil

T = TypeVar("T")

SETTINGS_FILE = 'sysmon.ini'
MAIN_FONT_FAMILY = "Source Sans Pro"
FIXED_FONT_FAMILY = "Source Code Pro"
DISK_ALERT_LEVEL = 80
DISK_WARN_LEVEL = 60
REFRESH_INTERVAL = 750  # milliseconds
INTERNAL_PAD = 12

BYTE_SYMBOLS = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB')

# SPDX-SnippetBegin
# SPDX-SnippetName bytes2human function
# http://code.google.com/p/pyftpdlib/source/browse/trunk/test/bench.py
# SPDX-FileCopyrightText: © 2007-2013 Giampaolo Rodola' <g.rodola@gmail.com>
# SPDX-License-Identifier: MIT


def bytes2human(num: int, precision: int = 1) -> str:
    """
    Convert a byte count to a human-readable format, with a given precision.

    Parameters
    ----------
    num : int
        The number to format.
    precision : int, optional
        The number of decimals to use for display.

    Returns
    -------
    str
        The number in human-readable format.

    Examples
    --------
    >>> bytes2human(10000)
    '9.8KiB'
    >>> bytes2human(100001221)
    '95.4MiB'
    """
    # originally taken from pyftpdlib, then rewritten
    prefix = {}
    for idx, symb in enumerate(BYTE_SYMBOLS[1:]):
        prefix[symb] = 1 << (idx+1)*10
    for symbol in reversed(BYTE_SYMBOLS[1:]):
        if num >= prefix[symbol]:
            value = float(num) / prefix[symbol]
            return f"{value:.{precision}f}{symbol}"
    return f"{num:.{precision}f}{BYTE_SYMBOLS[0]}"

# SPDX-SnippetEnd


def bytes2whole(num: int):
    """
    Convert a byte count to a human-readable format, with no decimal.

    Parameters
    ----------
    num : int
        The number to format.

    Returns
    -------
    str
        The number in human-readable format.

    Examples
    --------
    >>> bytes2whole(10000)
    '10KiB'
    >>> bytes2whole(100001221)
    '95MiB'
    """
    return bytes2human(num, precision=0)


def digits(numstr: str) -> List[int]:
    """
    Return a list of numbers in a string.

    Parameters
    ----------
    numstr : str
        A string containing various numbers.

    Returns
    -------
    List[int]
        A list of integers extracted from the string.

    Examples
    --------
    >>> digits("")
    []
    >>> digits("8.5MiB")
    [8, 5]
    >> digits("13. Notes vol. 22, pp. 585-588, 1996.")
    [13, 22, 585, 588, 1996]
    """
    return [int(s) for s in re.findall(r'\d+', numstr)]


def cpu_temp(as_string: bool = False) -> Union[float, str]:
    """
    Return the CPU temperature, either formatted as a string, or as a float.

    Parameters
    ----------
    as_string: bool
        a flag indicating whether to return a string or a float.

    Returns
    -------
    float | str
        The current CPU temperature, possibly formatted as a string.

    Examples
    --------
    >>> cpu_temp(as_string: True)
    "41.0°C"
    >>> cpu_temp(False)
    41.0
    """
    temps = psutil.sensors_temperatures()
    key = 'coretemp' if 'coretemp' in temps else list(temps)[0]
    return f"{temps[key][0].current}°C" if as_string else temps[key][0].current


def net_addr() -> str:
    """
    Get the first non-loopback network address.

    Returns
    -------
    str
        The discovered network address.
    """
    addresses = psutil.net_if_addrs()
    for nic, addr_list in addresses.items():
        if nic != "lo":
            addr = [addr.address for addr in addr_list if addr.family == AF_INET]
            return addr[0] if len(addr) > 0 else ""
    return ""


def system_uptime() -> str:
    """
    Return the system uptime in a human-readable format.

    Returns
    -------
    str
        The current system uptime in a human-readable format.

    Examples
    --------
    >>> system_uptime()  # for a system just rebooted
    "47 sec"
    >>> system_uptime()  # five minutes later
    "5m 47s"
    >>> system_uptime()  # 2 hours later
    "2h 5m 47s"
    >>> system_uptime()  # 8 days later
    "8d 2h 5m"
    """
    uptime = time.time() - psutil.boot_time()
    uptime_minutes, uptime_seconds = divmod(uptime, 60)
    uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)
    uptime_days, uptime_hours = divmod(uptime_hours, 24)
    if uptime_days:
        return f"{uptime_days:.0f}d {uptime_hours:.0f}h {uptime_minutes:.0f}m"
    if uptime_hours:
        return f"{uptime_hours:.0f}h {uptime_minutes:.0f}m {uptime_seconds:.0f}s"
    if uptime_minutes:
        return f"{uptime_minutes:.0f}m {uptime_seconds:.0f}s"
    return f"{uptime_seconds:.0f} sec"


def disk_usage(mountpoint: str) -> str:
    """
    Return the disk usage of the provided mount point in a human-readable format.

    Parameters
    ----------
    mountpoint: str
        a filesystem path belonging to the desired mount point.

    Returns
    -------
    str
        A human-readable string of the disk usage.

    Example
    -------
    >>> disk_usage("/")
    "32GiB/199GiB 17%"
    """
    diskinfo = psutil.disk_usage(mountpoint)
    used_fmt = bytes2whole(diskinfo.used)
    total_fmt = bytes2whole(diskinfo.total)
    # if formatted numbers are less then 10, use single decimal place rather than zero decimals
    if digits(used_fmt)[0] < 10:
        used_fmt = bytes2human(diskinfo.used)
    if digits(total_fmt)[0] < 10:
        total_fmt = bytes2human(diskinfo.total)
    return f"{used_fmt}/{total_fmt} {round(diskinfo.percent)}%"


def is_dark(hexcolor: str) -> bool:
    """
    Determine whether a given hex color is light or dark.

    Parameters
    ----------
    hexcolor: str
        a string with the format "#xxxxxx" where x is a hex digit (0-9, A-F)

    Returns
    -------
    bool
        True when the color is determined to be dark; False otherwise.

    Examples
    --------
    >>> is_dark("#000000")
    True
    >>> is_dark("#ffffff")
    False
    >>> is_dark("#123456")
    True
    >>> is_dark("#449F55")
    False
    """
    assert len(hexcolor) == 7  # nosec B101
    assert hexcolor[:1] == "#"  # nosec B101
    if re.search(r"^#[\dA-Fa-f]{6}$", hexcolor) is None:
        raise ValueError("hexcolor must start with '#' and have 6 hexadecimal digits")
    r = int(hexcolor[1:3], 16)
    g = int(hexcolor[3:5], 16)
    b = int(hexcolor[5:7], 16)
    # calculate the square of the luminance and compare it to a cutoff value of 127.5²
    # this way, sqrt() doesn't need to be called
    hsp = 0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b)
    return hsp < 16256.25


def get_processor_name() -> str:
    """
    Get the full processor name of the computer running.
    """
    if platform.system() == "Windows":
        return platform.processor()
    if platform.system() == "Darwin":
        return subprocess.check_output(  # nosec B603
            ["/usr/sbin/sysctl", "-n", "machdep.cpu.brand_string"]
        ).decode("utf-8").strip()
    if platform.system() == "Linux":
        all_info = subprocess.check_output(  # nosec B603
            ["/usr/bin/cat", "/proc/cpuinfo"]
        ).decode().strip()
        for line in all_info.split("\n"):
            if "model name" in line:
                return re.sub(".*model name.*:", "", line, 1)
    return ""


def get_full_path(relative_path: str) -> str:
    """
    Get the full path of a file, based on its relative path to this project.
    """
    return f"{os.path.realpath(os.path.dirname(__file__))}/{relative_path}"


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
