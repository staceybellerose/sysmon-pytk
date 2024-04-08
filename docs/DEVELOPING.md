# Local Development

<!--
SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>

SPDX-License-Identifier: MIT
-->

A `Makefile` has been configured to make working with the package easier. It
expects to be used with GNU make 4.0 or later. Many commands below use the
`make` command instead of several lines of scripting. To see the basic options
available in the `Makefile`, run `make help`.

## Clone the repository

Note when cloning this repo that it has a submodule
[Azure ttk theme](https://github.com/staceybellerose/Azure-ttk-theme)
which must be copied over:

```bash
git clone --recurse-submodules https://github.com/staceybellerose/sysmon-pytk.git
```

If you didn't clone the submodule when cloning this repo, run this to update:

```bash
git submodule update --init --recursive
```

## Install the required python packages

```bash
make venv
```

This will create a virtual environment and install the required packages (in
`requirements.txt` and `requirements-dev.txt`). The packages listed in
`requirements-dev.txt` are only required to build the application, but not to
run it.

## Generate translation files

Translations are available in English, Spanish, German, and Norwegian Bokmål.

```bash
make translations
```

## (Re-)generate image files

Images needed for the application are already commited in this repository, but
can be rebuilt from sources (either SVG or extracted from a tarball) if desired.

```bash
make images
```

This will extract all images from the tarball and convert them, as well as
convert the SVG images into PNG to be usable by the application.

Regenerating the images requires [imagemagick](https://imagemagick.org/).

## Run various linter programs

```bash
make lint
```

The following linters are installed via `requirements-dev.txt` and configured:

* ruff - all-purpose linter
* isort - import definition sorting
* pylint - linter
* mypy - type hinting validation
* pycodestyle - check code style against PEP8
* pydocstyle - docstring linter
* pyflakes - code error linter
* bandit - security issue checker
* reuse - validate REUSE specification for copyrights
* liccheck - validate license compliance of dependencies
* radon - code metric calculations
* msgcmp - gettext utility to look for missing translations
* pyroma - to validate the build artifacts comply with best practices

Radon is used to determine
[cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)
of the code, to make sure no function is overly complex. It is also used to
check the total source lines of code (code lines plus docstrings) per module,
so no over-long modules are created.

## Run the GUI program

| | |
|-|-|
| While the venv is activated | `python -m sysmon_pytk.gui_sysmon &` |
| Explicitly using the venv | `venv/bin/python -m sysmon_pytk.gui_sysmon &` |
| Let make handle everything automatically | `make run` or `make gui` |

## Run the command line program

| | |
|-|-|
| While the venv is activated | `python -m sysmon_pytk.cli_sysmon &` |
| Explicitly using the venv | `venv/bin/python -m sysmon_pytk.cli_sysmon &` |
| Let make handle everything automatically | `make cli` |

## Build the package

```bash
make build
```

This will build the sdist and then the wheel, copying them into the `dist`
folder.

## Build the API documentation

```bash
make apidocs
```

After building the API docs, they are available in the `apidocs/sysmon_pytk/`
folder.
