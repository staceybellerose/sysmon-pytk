# System Monitor for Python/Tk

<!--
SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>

SPDX-License-Identifier: MIT
-->
<!-- markdownlint-disable MD033 -->

[![GitHub License](https://img.shields.io/github/license/staceybellerose/sysmon-pytk?color=7C4DFF)](https://opensource.org/license/MIT)
[![GitHub Release](https://img.shields.io/github/v/release/staceybellerose/sysmon-pytk)](https://github.com/staceybellerose/sysmon-pytk/releases)
[![AppVeyor Build](https://img.shields.io/appveyor/build/staceybellerose/sysmon-pytk/main?logo=appveyor&logoColor=white)](https://ci.appveyor.com/project/staceybellerose/sysmon-pytk/)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/staceybellerose/sysmon-pytk/docs.yml?logo=github&logoColor=white&label=docs)](https://staceybellerose.github.io/sysmon-pytk/)

[![PyPI - Status](https://img.shields.io/pypi/status/sysmon-pytk)](https://pypi.org/project/sysmon-pytk/)
[![PyPI - Version](https://img.shields.io/pypi/v/sysmon-pytk)](https://pypi.org/project/sysmon-pytk/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sysmon-pytk)](https://pypi.org/project/sysmon-pytk/)

[![REUSE status](https://api.reuse.software/badge/github.com/staceybellerose/sysmon-pytk)](https://api.reuse.software/info/github.com/staceybellerose/sysmon-pytk)
[![CodeFactor Grade](https://img.shields.io/codefactor/grade/github/staceybellerose/sysmon-pytk?logo=codefactor)](https://www.codefactor.io/repository/github/staceybellerose/sysmon-pytk)
[![Maintainability](https://api.codeclimate.com/v1/badges/556c93bf800d0d58e7e4/maintainability)](https://codeclimate.com/github/staceybellerose/sysmon-pytk/maintainability)

System monitor written in Python using the Tk library. It monitors CPU usage and
temperature, RAM usage, and disk usage of the primary disk (containing the
root partition). It also displays the system's hostname, IP address, uptime,
and current process count.

![Main Window](images/main_window.png)

## Pre-installation

Make sure the Python interface to Tcl/Tk (tkinter) is installed.

[tkinter Installation Instructions](https://github.com/staceybellerose/sysmon-pytk/blob/main/docs/PRE-INSTALLATION.md)

## Install Using pip

```bash
pip install sysmon-pytk
```

Two versions of the program will be installed, a GUI program and a command line
program.

## Run the GUI program

```bash
sysmon
```

or

```bash
gui_sysmon
```

## Run the command line program

```bash
cli_sysmon
```

To get available options for the command line program, use `cli_sysmon -h`, or
[read them online](https://github.com/staceybellerose/sysmon-pytk/blob/main/docs/CLI_USAGE.md).

## Translations

Special thanks to our translators!

| Language         | Code  | Translator |
|------------------|-------|------------|
| German           | de    | Alisyn Arness, [Rainer Schwarzbach](https://github.com/blackstream-x) |
| Spanish          | es    | Stacey Adams (author), [Félix Medrano](https://github.com/robertxgray) |
| Norwegian Bokmål | nb_NO | [Allan Nordhøy](https://github.com/comradekingu) |

## Contributing

Translations are always welcome! The strings to be translated are located in
[app.pot](https://github.com/staceybellerose/sysmon-pytk/blob/main/sysmon_pytk/locale/app.pot)
and
[argparse.pot](https://github.com/staceybellerose/sysmon-pytk/blob/main/sysmon_pytk/locale/argparse.pot).

`argparse.pot` contains standard strings from the Python Standard Library file
`argparse.py` (Python versions 3.9–3.12).

If you want to work on the code, read the
[Development Guide](https://github.com/staceybellerose/sysmon-pytk/blob/main/docs/DEVELOPING.md).
Also, check out the [API Documentation](https://staceybellerose.github.io/sysmon-pytk/).

Contributers are expected to follow our
[Code of Conduct](https://github.com/staceybellerose/sysmon-pytk/blob/main/CODE_OF_CONDUCT.md).

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

