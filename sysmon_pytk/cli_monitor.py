#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Command line system monitor.
"""

import gettext
import sys
import time
from socket import gethostname
from typing import NoReturn

import psutil
from blessings import Terminal

from . import _common, about
from .app_locale import LANGUAGES, get_translator

_ = get_translator()

# set up argparse translation
gettext.gettext = get_translator(domain="argparse")

# Don't move this to the top of the import list! gettext must be imported first
# and gettext.gettext must be reassigned for argparse translations to work.

import argparse  # noqa: E402 # pylint: disable=C0411,C0413

REFRESH_SLEEP = 1.0
TOTAL_BLOCKS = 50

term = Terminal()

# ruff: noqa: T201


def _get_usage_color(percent: float) -> str:
    if percent > _common.DISK_ALERT_LEVEL:
        return term.bright_red
    if percent > _common.DISK_WARN_LEVEL:
        return term.bright_yellow
    return term.bright_green


def _cpu_usage() -> str:
    percent = psutil.cpu_percent(interval=None)
    label = _("CPU Usage") + ": "
    details = f"{percent}%"
    hilite = _get_usage_color(percent)
    return label + hilite + details + term.normal + " "*5


def _cpu_temp() -> str:
    temperature = _common.cpu_temp()
    label = _("Temperature") + ": "
    details = f"{temperature}°C"
    hilite = _get_usage_color(temperature)
    return label + hilite + details + term.normal + " "*5


def _mem_usage() -> str:
    meminfo = psutil.virtual_memory()
    used = _common.bytes2human(meminfo.total - meminfo.available)
    total = _common.bytes2human(meminfo.total)
    label = _("RAM Usage") + ": "
    details = f"{used}/{total} {round(meminfo.percent)}%"
    hilite = _get_usage_color(meminfo.percent)
    return label + hilite + details + term.normal + " "*5


def _swap_usage() -> str:
    meminfo = psutil.swap_memory()
    used = _common.bytes2human(meminfo.used)
    total = _common.bytes2human(meminfo.total)
    label = _("Swap Memory") + ": "
    details = f"{used}/{total} {round(meminfo.percent)}%"
    hilite = _get_usage_color(meminfo.percent)
    return label + hilite + details + term.normal + " "*5


def _disk_usage(mountpoint: str) -> str:
    usage = psutil.disk_usage(mountpoint)
    used = _common.bytes2human(usage.used)
    total = _common.bytes2human(usage.total)
    details = f"{used}/{total} {round(usage.percent)}%"
    hilite = _get_usage_color(usage.percent)
    return hilite + details + term.normal + " "*5


def _disk_usage_rjust(mountpoint: str, width: int) -> str:
    usage = psutil.disk_usage(mountpoint)
    used = _common.bytes2human(usage.used)
    total = _common.bytes2human(usage.total)
    details = f"{used}/{total} {round(usage.percent)}%"
    hilite = _get_usage_color(usage.percent)
    return hilite + details.rjust(width) + term.normal


def _disk_usage_bar(mountpoint: str) -> str:
    usage = psutil.disk_usage(mountpoint)
    used_blocks = int(usage.percent * TOTAL_BLOCKS / 100)
    empty_blocks = TOTAL_BLOCKS - used_blocks
    details = "█" * used_blocks + "━" * empty_blocks
    hilite = _get_usage_color(usage.percent)
    return hilite + details + term.normal + " "*5


def _disk_details(*, starting_line: int) -> None:
    print(
        term.move(starting_line, 1) + term.black_on_bright_white
        + _("Disk Usage").upper() + term.normal
    )
    for idx, part in enumerate(psutil.disk_partitions()):
        line = 2*idx + starting_line + 1
        if line + 1 > term.height:
            break
        mountpoint = part.mountpoint
        print(term.move(line, 0) + " "*(term.width-1))
        print(term.move(line, 1) + mountpoint + term.el)
        print(term.move(line + 1, 1) + _disk_usage_bar(mountpoint))
        print(term.move(line + 1, TOTAL_BLOCKS + 3) + _disk_usage(mountpoint) + term.el)
    print(term.clear_eos)


def _temp_details(*, starting_line: int) -> None:
    print(
        term.move(starting_line, 1) + term.black_on_bright_white
        + _("Temperature Sensors").upper() + term.normal
    )
    temps = psutil.sensors_temperatures()
    line = starting_line + 1
    for name, entries in temps.items():
        if line + len(entries) + 1 > term.height:
            break
        print(term.move(line, 0) + " " + term.magenta + name + term.normal + term.el)
        line += 1
        for entry in entries:
            tag = (entry.label or name).ljust(20) + " "
            display = _("{current}°C (high = {high}°C, critical = {critical}°C)").format(
                current=entry.current, high=entry.high, critical=entry.critical
            )
            print(term.move(line, 0) + " "*10 + tag + display + term.el)
            line += 1
    print(term.clear_eos)


def blank_below_line(line: int, start_col: int, width: int) -> None:
    """
    Blank a rectangular section of the screen with spaces.
    """
    for row in range(line, term.height-1):
        print(term.move(row, start_col) + " "*width)


def _disk_details_half(*, starting_line: int) -> None:
    allowed_width = term.width//2 - 1
    print(
        term.move(starting_line, 1) + term.black_on_bright_white
        + _("Disk Usage").upper() + term.normal
    )
    partitions = psutil.disk_partitions()
    for idx, part in enumerate(partitions):
        line = 2*idx + starting_line + 1
        if line + 1 > term.height:
            break
        mountpoint = part.mountpoint
        print(term.move(line, 1) + mountpoint.ljust(allowed_width))
        print(term.move(line + 1, 1) + _disk_usage_rjust(mountpoint, allowed_width))
    blank_below_line(2*len(partitions) + starting_line + 1, 1, allowed_width)


def _temp_details_half(*, starting_line: int) -> None:
    start_col = term.width//2 + 1
    print(
        term.move(starting_line, start_col) + term.black_on_bright_white
        + _("Temperature Sensors").upper() + term.normal
    )
    temps = psutil.sensors_temperatures()
    line = starting_line + 1
    for name, entries in temps.items():
        if line + len(entries) + 1 > term.height:
            break
        print(term.move(line, start_col) + term.magenta + name + term.normal + term.el)
        line += 1
        for entry in entries:
            label_width = term.width//2 - 7
            print(
                term.move(line, start_col) + " "*5
                + (entry.label or name).ljust(label_width)[:label_width]
            )
            print(term.move(line, term.width-11) + f"{entry.current}°C".rjust(10))
            line += 1
    blank_below_line(line, start_col, term.width-start_col)


def monitor_system(args: argparse.Namespace) -> NoReturn:
    """
    Monitor the system usage.
    """
    app_title = _("System Monitor").upper()
    while True:
        print(term.move(0, 1) + term.black_on_bright_white + app_title + term.normal)
        print(term.move(1, 1) + _("Hostname: {}").format(gethostname()) + term.el)
        print(term.move(1, 31) + _("IP Address: {}").format(_common.net_addr()) + term.el)
        print(term.move(2, 1) + _("Processes: {}").format(len(psutil.pids())) + term.el)
        print(term.move(2, 31) + _("Uptime: {}").format(_common.system_uptime()) + term.el)
        print(term.move(4, 1) + _cpu_usage())
        print(term.move(5, 1) + _cpu_temp())
        print(term.move(4, 31) + _mem_usage())
        print(term.move(5, 31) + _swap_usage())
        start = 7
        if args.details == "d":
            _disk_details(starting_line=start)
        elif args.details == "t":
            _temp_details(starting_line=start)
        elif args.details == "b":
            _disk_details_half(starting_line=start)
            _temp_details_half(starting_line=start)
        msg = _("<Ctrl-C> to quit")
        print(
            term.move(term.height-1, term.width-len(msg)-1)
            + term.cyan + msg + term.normal + term.move(0, 0)
        )
        time.sleep(args.refresh)


def _get_parser() -> argparse.Namespace:
    app_desc = _(
        "System monitor: display CPU usage/temperature, memory usage, disk usage"
    )
    epilog = _(
        "By default, this program will use the same language as that selected "
        "for the GUI application. To override it, use the '-l' option. To "
        "quit, press <Ctrl-C>."
    )
    parser = argparse.ArgumentParser(
        description=app_desc, epilog=epilog, add_help=False
    )
    options = parser.add_argument_group(_("Options"))
    options.add_argument(
        "-h", "-?", "--help", action="help",
        help=_("show this help message and exit")
    )
    options.add_argument(
        "-v", "--version", action="version",
        version=f"{about.__app_name__} {about.__version__}",
        help=_("show program's version number and exit")
    )
    options.add_argument(
        "-r", "--refresh", type=float, default=REFRESH_SLEEP, metavar="TIME",
        help=_("time between screen refreshes (in seconds, default=%(default)s)")
    )
    options.add_argument(
        "-l", "--language", choices=LANGUAGES.values(),
        help=_("the language to use for display")
    )
    detail_options = parser.add_argument_group(_("Display Details"))
    details = detail_options.add_mutually_exclusive_group()
    details.add_argument(
        "-d", "--disk", action="store_const", dest="details", const="d",
        help=_("show disk details (default)")
    )
    details.add_argument(
        "-t", "--temperature", action="store_const", dest="details", const="t",
        help=_("show temperature details")
    )
    details.add_argument(
        "-b", "--both", action="store_const", dest="details", const="b",
        help=_("show both disk and temperature details")
    )
    details.add_argument(
        "-x", "--no-details", action="store_const", dest="details", const="",
        help=_("show no details, only the header")
    )
    parser.set_defaults(details="d")
    return parser.parse_args()


def cli_monitor() -> NoReturn:
    """
    Entry point for CLI monitor.
    """
    args = _get_parser()
    global _  # noqa: PLW0603 # pylint: disable=global-statement
    _ = get_translator(forced_lang=args.language)
    print(term.enter_fullscreen() + term.clear + term.civis)
    try:
        monitor_system(args)
    except KeyboardInterrupt:
        print(term.cnorm + term.clear + term.exit_fullscreen())
        sys.exit(0)


if __name__ == "__main__":
    cli_monitor()
