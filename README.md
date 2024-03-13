# System Monitor for python/Tk

<!--
SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>

SPDX-License-Identifier: MIT
-->

![GitHub License](https://img.shields.io/github/license/staceybellerose/sysmon-pytk)
[![REUSE status](https://api.reuse.software/badge/github.com/staceybellerose/sysmon-pytk)](https://api.reuse.software/info/github.com/staceybellerose/sysmon-pytk)
[![CodeFactor](https://www.codefactor.io/repository/github/staceybellerose/sysmon-pytk/badge)](https://www.codefactor.io/repository/github/staceybellerose/sysmon-pytk)

System monitor written in Python using Tk. It monitors CPU usage and
temperature, RAM usage, and disk usage of the primary disk (containing the
root partition). It also displays the system's hostname, IP address, uptime,
and current process count.

## Installation

Note when cloning this repo that it has a submodule
[Azure ttk theme](https://github.com/rdbende/Azure-ttk-theme)
which must be copied over:

```bash
git clone --recurse-submodules https://github.com/staceybellerose/sysmon-pytk.git
```

### Install the Python interface to Tcl/Tk (tkinter)

* Debian, Ubuntu, and derivatives

    ```bash
    sudo apt install python3-tk
    ```

* Fedora and derivatives

    ```bash
    sudo dnf install python3-tkinter
    ```

* MacOS

    ```bash
    brew install python-tk
    ```

### Install the required python packages

```bash
make venv
```

### Generate translation files

Translations are available in English, Spanish, German, and Norwegian Bokmål.
To build the translation files, run the following bash commands:

```bash
make translations
```

## Running

```bash
# While the venv is activated
python -m sysmon_pytk.gui_monitor &
```

OR

```bash
# Explicitly using the venv
venv/bin/python -m sysmon_pytk.gui_monitor &
```

OR

```bash
# Let make handle everything automatically
make run
```

## Translations

Special thanks to our translators!

| Language | Translator |
|----------|------------|
| Spanish  | Stacey Adams |
| German   | Alisyn Arness |
| Norwegian Bokmål | [Allan Nordhøy](https://github.com/comradekingu) |
