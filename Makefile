# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

SHELL := /bin/bash
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Don't use Tab to indent recipes: some editors aggressively replace tabs with spaces,
# which would break everything.
ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

VENV := venv
LOCALE := locale
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYLINT := $(VENV)/bin/pylint
MYPY := $(VENV)/bin/mypy
PYCODESTYLE := $(VENV)/bin/pycodestyle
PYDOCSTYLE := $(VENV)/bin/pydocstyle
PYFLAKES := $(VENV)/bin/pyflakes
REUSE := $(VENV)/bin/reuse
BANDIT := $(VENV)/bin/bandit
RADON := $(VENV)/bin/radon
TWINE := $(VENV)/bin/twine

# make sure all external programs are available
EXECUTABLES = python3 awk sort
K := $(foreach exec,$(EXECUTABLES), $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.DEFAULT_GOAL := help

.PHONY: translations pylint mypy pycodestyle pydocstyle bandit reuse build sdist wheel clean help

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
> python3 -m venv $(VENV)
> $(PIP) install -r requirements.txt
> $(PIP) install -r requirements-dev.txt

##@ Dependencies

venv: $(VENV)/bin/activate  ## Build Python virtual environment

translations:  ## Make translations
> $(MAKE) -C sysmon_pytk/locale all

##@ Running

cli: $(VENV)/bin/activate translations  ## Run the command line application
> $(PYTHON) -m sysmon_pytk.cli_monitor

gui: run

run: $(VENV)/bin/activate translations  ## Run the GUI application
> $(PYTHON) -m sysmon_pytk.gui_monitor &

##@ Testing

lint: pyflakes pylint mypy pycodestyle pydocstyle bandit reuse  ## All lint and static code checks

pylint:  ## Code lint check
> $(PYLINT) --verbose sysmon_pytk

mypy:  ## Validate type hinting
> $(MYPY) sysmon_pytk

pycodestyle:  ## Check code style against PEP8
> $(PYCODESTYLE) --benchmark --verbose sysmon_pytk

pydocstyle:  ## Check dotstrings
> $(PYDOCSTYLE) --verbose sysmon_pytk

pyflakes:  ## Code error linter
> $(PYFLAKES) sysmon_pytk

bandit:  ## Check for common security issues
> $(BANDIT) -r sysmon_pytk

reuse:  ## Verify REUSE Specification for Copyrights
> $(REUSE) lint

##@ Metrics

metrics: radon-raw radon-cc radon-mi  ## All code metric calculations

radon-cc:  ## Cyclomatic Complexity of codebase
> $(RADON) cc sysmon_pytk

radon-mi:  ## Maintainability Index of codebase
> $(RADON) mi sysmon_pytk | sort -t "(" -k 2 -g -r

radon-raw:  ## Raw metrics of codebase
> $(RADON) raw sysmon_pytk --summary

##@ Publishing

build:  ## Build both source and binary distribution files
> $(PYTHON) -m build

sdist:  ## Build only a source distribution
> $(PYTHON) -m build --sdist

wheel:  ## Build only a binary distribution (wheel)
> $(PYTHON) -m build --wheel

upload-check: dist/*.tar.gz dist/*.whl  ## Check the dist files before uploading
> $(TWINE) check dist/*

upload-test: dist/*.tar.gz dist/*.whl  ## Upload the package to TestPyPI
> $(TWINE) upload --repository testpypi dist/*

upload: dist/*.tar.gz dist/*.whl  ## Upload the package to PyPI
> $(TWINE) upload dist/*

##@ Cleanup

clean:  ## Clean up the project folders
> rm -rf __pycache__
> rm -rf dist
> rm -rf sysmon_pytk.egg-info
> $(MAKE) -C locale clean

##@ Helpers

help:  ## Display this help
> @awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
