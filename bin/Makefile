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
VENV := ../venv

# required programs
AWK = /usr/bin/awk
SORT = /usr/bin/sort
JQ = /usr/bin/jq

# tools installed by pip
BANDIT := $(VENV)/bin/bandit
ISORT := $(VENV)/bin/isort
MYPY := $(VENV)/bin/mypy
PYCODESTYLE := $(VENV)/bin/pycodestyle
PYDOCSTYLE := $(VENV)/bin/pydocstyle
PYFLAKES := $(VENV)/bin/pyflakes
PYLINT := $(VENV)/bin/pylint
RADON := $(VENV)/bin/radon
RUFF := $(VENV)/bin/ruff

srcs := $(wildcard ./*.py)

# make sure all external programs are available
EXECUTABLES = $(AWK) $(SORT) $(JQ)
K := $(foreach exec,$(EXECUTABLES), \
$(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.DEFAULT_GOAL := help

.PHONY: ruff ruff-fix isort isort-fix pylint mypy pycodestyle pydocstyle
.PHONY: bandit loc help

##@ Testing

lint: ruff isort pyflakes mypy pycodestyle pydocstyle bandit loc pylint  ## All lint and static code checks

ruff:  ## Code lint check
> $(RUFF) check --config ../pyproject.toml $(srcs)

ruff-fix:  ## Code lint check, and apply safe fixes
> $(RUFF) check --config ../pyproject.toml --fix $(srcs)

isort:  ## Check sortation of import definitions
> $(ISORT) --settings-file ../setup.cfg --check $(srcs)

isort-fix:  ## Resort import definitions
> $(ISORT) --settings-file ../setup.cfg $(srcs)

pylint:  ## Code lint check
> $(PYLINT) --verbose --rcfile ../.pylintrc $(srcs)

mypy:  ## Validate type hinting
> $(MYPY) --config-file ../setup.cfg --cache-dir ../.mypy_cache $(srcs)

pycodestyle:  ## Check code style against PEP8
> $(PYCODESTYLE) --benchmark --verbose $(srcs)

pydocstyle:  ## Check dotstrings
> $(PYDOCSTYLE) --verbose --config=../setup.cfg $(srcs)

pyflakes:  ## Code error linter
> $(PYFLAKES) $(srcs)

bandit:  ## Check for common security issues
> $(BANDIT) -r $(srcs)

loc:  ## Complexity check (lines of code)
> $(RADON) raw --json $(srcs) | $(JQ) 'to_entries | map(.value |= .sloc+.multi | select(.value > $(LOC_MAX))) | sort_by('.value') | reverse | map(.value |= tostring) | reduce .[] as $$item (""; . + "\n" + $$item.key + " has " + $$item.value + " lines (max allowed = $(LOC_MAX))") | if (. | length) > 0 then error(.) else empty end'

##@ Metrics

metrics: radon-raw radon-cc radon-mi  ## All code metric calculations

radon-cc:  ## Cyclomatic Complexity of codebase
> $(RADON) cc --min B --show-complexity --total-average $(srcs)

radon-mi:  ## Maintainability Index of codebase
> $(RADON) mi --show $(srcs) | $(SORT) -t "(" -k 2 -g -r

radon-raw:  ## Raw metrics of codebase
> $(RADON) raw $(srcs) --summary

##@ Helpers

help:  ## Display this help
> @$(AWK) 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
