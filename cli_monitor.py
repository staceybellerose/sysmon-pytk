#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Command line system monitor.
"""

import sys
import time
from socket import gethostname

import psutil

import _common

REFRESH_SLEEP = 1.0


def _cpu_usage():
    return f"{psutil.cpu_percent(interval=None)}%"


def _mem_usage():
    meminfo = psutil.virtual_memory()
    used = _common.bytes2human(meminfo.used)
    total = _common.bytes2human(meminfo.total)
    return f"{used}/{total} {round(meminfo.percent)}%"


def monitor_system():
    """
    Monitor the system usage.
    """
    while True:
        print('Name:', gethostname())
        print('IP:', _common.net_addr())
        print('Uptime:', _common.system_uptime())
        print('')
        time.sleep(REFRESH_SLEEP)
        print('CPU:', _cpu_usage(), _common.cpu_temp(as_string=True))
        print('Mem:', _mem_usage())
        print('Disk:', _common.disk_usage('/'))
        print('')
        time.sleep(REFRESH_SLEEP)


if __name__ == '__main__':
    try:
        monitor_system()
    except KeyboardInterrupt:
        sys.exit(0)
