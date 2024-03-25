# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

SHELL = /bin/bash
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# Don't use Tab to indent recipes: some editors aggressively replace tabs with spaces,
# which would break everything.
ifeq ($(origin .RECIPEPREFIX), undefined)
  $(error This Make does not support .RECIPEPREFIX. Please use GNU Make 4.0 or later)
endif
.RECIPEPREFIX = >

# max lines of code allowed before "too complex"
LOC_MAX = 250
# directory to use for venv
VENV := venv

# required programs
AWK = /usr/bin/awk
SORT = /usr/bin/sort
JQ = /usr/bin/jq
# system-installed python, used to create venv
BASE_PYTHON = /usr/bin/python3

# tools installed by pip
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
BANDIT := $(VENV)/bin/bandit
ISORT := $(VENV)/bin/isort
LICCHECK := $(VENV)/bin/liccheck
MYPY := $(VENV)/bin/mypy
PYCODESTYLE := $(VENV)/bin/pycodestyle
PYDOCSTYLE := $(VENV)/bin/pydocstyle
PYFLAKES := $(VENV)/bin/pyflakes
PYROMA := $(VENV)/bin/pyroma
PYLINT := $(VENV)/bin/pylint
RADON := $(VENV)/bin/radon
REUSE := $(VENV)/bin/reuse
RUFF := $(VENV)/bin/ruff
TWINE := $(VENV)/bin/twine

srcs := $(wildcard ../*.py ../modals/*.py ../widgets/*.py)

# make sure all external programs are available
EXECUTABLES = $(BASE_PYTHON) $(AWK) $(SORT) $(JQ)
K := $(foreach exec,$(EXECUTABLES), $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.DEFAULT_GOAL := help

.PHONY: translations ruff ruff-fix isort isort-fix pylint mypy pycodestyle pydocstyle bandit reuse liccheck loc build sdist wheel clean help

$(VENV)/bin/activate: requirements.txt requirements-dev.txt
> $(BASE_PYTHON) -m venv $(VENV)
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

lint: ruff isort pyflakes mypy pycodestyle pydocstyle bandit loc pylint reuse liccheck  ## All lint and static code checks

ruff:  ## Code lint check
> $(RUFF) check sysmon_pytk

ruff-fix:  ## Code lint check, and apply safe fixes
> $(RUFF) check --fix sysmon_pytk

isort:  ## Check sortation of import definitions
> $(ISORT) --check sysmon_pytk

isort-fix:  ## Resort import definitions
> $(ISORT) sysmon_pytk

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

liccheck:  ## Validate licenses of dependencies
> $(LICCHECK) -l PARANOID

loc:  ## Complexity check (lines of code)
> $(RADON) raw --json sysmon_pytk | $(JQ) 'to_entries | map(.value |= .sloc+.multi | select(.value > $(LOC_MAX))) | sort_by('.value') | reverse | map(.value |= tostring) | reduce .[] as $$item (""; . + "\n" + $$item.key + " has " + $$item.value + " lines (max allowed = $(LOC_MAX))") | if (. | length) > 0 then error(.) else empty end'

##@ Metrics

metrics: radon-raw radon-cc radon-mi  ## All code metric calculations

radon-cc:  ## Cyclomatic Complexity of codebase
> $(RADON) cc sysmon_pytk

radon-mi:  ## Maintainability Index of codebase
> $(RADON) mi sysmon_pytk | $(SORT) -t "(" -k 2 -g -r

radon-raw:  ## Raw metrics of codebase
> $(RADON) raw sysmon_pytk --summary

##@ Publishing

build: dist  ## Build both source and binary distribution files

dist: $(srcs)
> mkdir dist
> $(PYTHON) -m build

dist/*.tar.gz: build
dist/*.whl: build

sdist:  ## Build only a source distribution
> $(PYTHON) -m build --sdist

wheel:  ## Build only a binary distribution (wheel)
> $(PYTHON) -m build --wheel

pyroma: dist/*.tar.gz  ## Check package for best practices
> $(PYROMA) dist/*.tar.gz

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
> $(MAKE) -C sysmon_pytk/locale clean

##@ Helpers

help:  ## Display this help
> @$(AWK) 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
