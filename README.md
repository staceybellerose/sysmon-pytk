# System Monitor for python/Tk

<!--
SPDX-FileCopyrightText: © 2024 2024 Stacey Adams <stacey.belle.rose@gmail.com>

SPDX-License-Identifier: MIT
-->

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
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

### Generate translation files

Translations are available in English and Spanish. To build the translation
files, run the following bash commands:

```bash
cd locale
for d in *
do
    if [ -d "$d" ]
    then
        pushd "$d/LC_MESSAGES"
        msgfmt -o app.mo app.po -v
        popd
    fi
done
```

## Running

```bash
(venv) $ python main.py &
```
