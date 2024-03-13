# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

SHELL = /bin/bash

VENV := venv
LOCALE := locale
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYLINT := $(VENV)/bin/pylint
MYPY := $(VENV)/bin/mypy
PYCODESTYLE := $(VENV)/bin/pycodestyle
PYDOCSTYLE := $(VENV)/bin/pydocstyle
REUSE := $(VENV)/bin/reuse

# make sure all external programs are available
EXECUTABLES = python3 awk
K := $(foreach exec,$(EXECUTABLES),\
    $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.DEFAULT_GOAL := help

.PHONY: translations pylint mypy pycodestyle pydocstyle bandit reuse clean help

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

##@ Dependencies

venv: $(VENV)/bin/activate  ## Build Python virtual environment

translations:  ## Make translations
	$(MAKE) -C sysmon_pytk/locale all

##@ Running

cli: $(VENV)/bin/activate translations  ## Run the command line application
	$(PYTHON) -m sysmon_pytk.cli_monitor

gui: run

run: $(VENV)/bin/activate translations  ## Run the GUI application
	$(PYTHON) -m sysmon_pytk.gui_monitor &

##@ Testing

lint: pylint mypy pycodestyle pydocstyle bandit reuse  ## All lint and static code checks

pylint:  ## Code lint check
	$(PYLINT) --verbose sysmon_pytk

mypy:  ## Validate type hinting
	$(MYPY) .

pycodestyle:  ## Check code style against PEP8
	$(PYCODESTYLE) --benchmark --verbose sysmon_pytk

pydocstyle:  ## Check dotstrings
	$(PYDOCSTYLE) --verbose sysmon_pytk

bandit:  ## Check for common security issues
	bandit --ini setup.cfg -r sysmon_pytk

reuse:  ## Verify REUSE Specification for Copyrights
	$(REUSE) lint

##@ Metrics

metrics: radon-cc radon-mi radon-raw  ## All code metric calculations

radon-cc:  ## Cyclomatic Complexity of codebase
	radon cc sysmon_pytk --total-average --show-complexity --min b

radon-mi:  ## Maintainability Index of codebase
	radon mi sysmon_pytk --show

radon-raw:  ## Raw metrics of codebase
	radon raw sysmon_pytk --summary

##@ Cleanup

clean:  ## Clean up the project folders
	rm -rf __pycache__
	$(MAKE) -C locale clean

##@ Helpers

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
