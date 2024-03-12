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
	$(MAKE) -C ./locale all

##@ Running

run: $(VENV)/bin/activate translations  ## Run the application
	$(PYTHON) main.py

##@ Testing

lint: pylint mypy pycodestyle pydocstyle bandit reuse  ## All lint and static code checks

pylint:  ## Code lint check
	$(PYLINT) --verbose .

mypy:  ## Validate type hinting
	$(MYPY) .

pycodestyle:  ## Check code style against PEP8
	$(PYCODESTYLE) --benchmark --verbose .

pydocstyle:  ## Check dotstrings
	$(PYDOCSTYLE) --verbose .

bandit:  ## Check for common security issues
	bandit -c bandit.yaml -r .

reuse:  ## Verify REUSE Specification for Copyrights
	$(REUSE) lint

##@ Cleanup

clean:  ## Clean up the project folders
	rm -rf __pycache__
	$(MAKE) -C locale clean

##@ Helpers

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
