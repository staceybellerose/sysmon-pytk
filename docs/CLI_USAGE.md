<!--
SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>

SPDX-License-Identifier: MIT
-->
<!-- markdownlint-disable MD041 MD033 -->

# Usage

usage: `cli_sysmon [-h] [-v] [-r TIME] [-l {en,es,de,nb_NO}] [-d | -t | -b | -x]`

System monitor: display CPU usage/temperature, memory usage, disk usage

## Options

| General Option | Details |
|----------------|---------|
| `-h`, `-?`, `--help` | show this help message and exit |
| `-v`, `--version`  | show program's version number and exit |
| `-r TIME`, `--refresh TIME` | time between screen refreshes (in seconds, default=1.0) |
| `-l {en,es,de,nb_NO}`,<br />`--language {en,es,de,nb_NO}` | the language to use for display |

## Display Details

| Display Option (choose one) | Details |
|----------------|---------|
| `-d`, `--disk` | show disk details (default) |
| `-t`, `--temperature` | show temperature details |
| `-b`, `--both` | show both disk and temperature details |
| `-x`, `--no-details` | show no details, only the header |

## Notes

By default, this program will use the same language as that selected for the
GUI application. To override it, use the `-l` option. To quit, press
<kbd>Ctrl-C</kbd>.
