# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Shared functions used throughout the application.
"""

from __future__ import annotations

import platform
import re
import subprocess  # nosec B404
import time
from socket import AF_INET

import psutil

DISK_ALERT_LEVEL = 80
DISK_WARN_LEVEL = 60
REFRESH_INTERVAL = 750  # milliseconds
INTERNAL_PAD = 12

BYTE_SYMBOLS = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")

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


def bytes2whole(num: int) -> str:
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


def digits(numstr: str) -> list[int]:
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
    return [int(s) for s in re.findall(r"\d+", numstr)]


def cpu_temp() -> float:
    """
    Return the CPU temperature, as a float.

    Returns
    -------
    float
        The current CPU temperature.

    Examples
    --------
    >>> cpu_temp()
    41.0
    """
    temps = psutil.sensors_temperatures()
    key = "coretemp" if "coretemp" in temps else next(iter(temps))
    return temps[key][0].current


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
    if digits(used_fmt)[0] < 10:  # noqa: PLR2004
        used_fmt = bytes2human(diskinfo.used)
    if digits(total_fmt)[0] < 10:  # noqa: PLR2004
        total_fmt = bytes2human(diskinfo.total)
    return f"{used_fmt}/{total_fmt} {round(diskinfo.percent)}%"


def get_processor_name() -> str:
    """
    Get the full processor name of the computer running.
    """
    if platform.system() == "Windows":
        return _get_processor_name_windows()
    if platform.system() == "Darwin":
        return _get_processor_name_darwin()
    if platform.system() == "Linux":
        return _get_processor_name_linux()
    return ""


def _get_processor_name_windows() -> str:
    return platform.processor()


def _get_processor_name_darwin() -> str:
    return subprocess.check_output(  # nosec B603
        ["/usr/sbin/sysctl", "-n", "machdep.cpu.brand_string"]
    ).decode("utf-8").strip()


def _get_processor_name_linux() -> str:
    all_info = subprocess.check_output(  # nosec B603
        ["/usr/bin/cat", "/proc/cpuinfo"]
    ).decode().strip()
    for line in all_info.split("\n"):
        if "model name" in line:
            return re.sub(r".*model name.*:", "", line, count=1)
    return ""
