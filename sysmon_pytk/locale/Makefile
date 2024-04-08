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

# required programs
AWK = /usr/bin/awk
MSGCMP = /usr/bin/msgcmp
MSGMERGE = /usr/bin/msgmerge
MSGFMT = /usr/bin/msgfmt
XGETTEXT = /usr/bin/xgettext

WIDTH = 79

srcs := $(wildcard ../*.py ../modals/*.py ../widgets/*.py)

# make sure all external programs are available
EXECUTABLES = $(XGETTEXT) $(MSGFMT) $(MSGMERGE) $(AWK)
K := $(foreach exec,$(EXECUTABLES), \
$(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

DOMAIN = $(shell $(AWK) '$$0 ~ "^__i18n_domain__" { gsub(/"/, ""); print $$2 }' FS=" = " ../app_locale.py)
PACKAGE = $(shell $(AWK) '$$0 ~ "^__app_name__" { gsub(/"/, ""); print $$2 }' FS=" = " ../about.py)
VERSION = $(shell $(AWK) '$$0 ~ "^__version__" { gsub(/"/, ""); print $$2 }' FS=" = " ../about.py)
AUTHOR = $(shell $(AWK) '$$0 ~ "^__author_name__" { gsub(/"/, ""); print $$2 }' FS=" = " ../about.py)
AUTHOR_EMAIL = $(shell $(AWK) '$$0 ~ "^__author_email__" { gsub(/"/, ""); print $$2 }' FS=" = " ../about.py)
COPYRIGHT_HOLDER = $(AUTHOR) <$(AUTHOR_EMAIL)>
MSGID_BUGS_ADDRESS = $(AUTHOR_EMAIL)

PYTHON = ../../venv/bin/python
PYTHONLIBS := $(wildcard /usr/lib/python3.*/argparse.py)
SUBDIRS := $(wildcard */LC_MESSAGES/.)

.DEFAULT_GOAL := help

.PHONY: pot po mo clean help all

all: pot po mo  ## Regenerate all translation files

pot: $(DOMAIN).pot argparse.pot  ## Regenerate POT file

po: $(SUBDIRS:.=$(DOMAIN).po) $(SUBDIRS:.=argparse.po)  ## Update PO files

mo: $(SUBDIRS:.=$(DOMAIN).mo) $(SUBDIRS:.=argparse.mo)  ## Compile MO files

$(DOMAIN).pot: $(srcs)
> $(XGETTEXT) --default-domain="$(DOMAIN)" --output="$(DOMAIN).pot" --verbose \
> --add-location=full --width=$(WIDTH) --copyright-holder="$(COPYRIGHT_HOLDER)" \
> --package-name="$(PACKAGE)" --package-version="$(VERSION)" \
> --msgid-bugs-address="$(MSGID_BUGS_ADDRESS)" $^

argparse.pot: $(PYTHONLIBS)
> $(XGETTEXT) --default-domain="argparse" --output="argparse.pot" --verbose \
> --add-location=full --width=$(WIDTH) --copyright-holder="$(COPYRIGHT_HOLDER)" \
> --package-name="i18nparse" --msgid-bugs-address="$(MSGID_BUGS_ADDRESS)" $^

define gen-po =
@if [ -f "$@" ] \
; then \
echo $(MSGMERGE) --add-location=full --width=$(WIDTH) --previous --update $@ $< \
; $(MSGMERGE) --add-location=full --width=$(WIDTH) --previous --update $@ $< \
; else \
echo cp -v $< $@ \
; cp -v $< $@ \
; fi
@touch -d yesterday $(@D)/$(shell basename $(@) .po).mo
@touch $@
endef

%/LC_MESSAGES/$(DOMAIN).po: $(DOMAIN).pot
> $(gen-po)

%/LC_MESSAGES/$(DOMAIN).mo: %/LC_MESSAGES/$(DOMAIN).po
> $(MSGFMT) --verbose --output-file=$@ $<

%/LC_MESSAGES/argparse.po: argparse.pot
> $(gen-po)

%/LC_MESSAGES/argparse.mo: %/LC_MESSAGES/argparse.po
> $(MSGFMT) --verbose --output-file=$@ $<

lint: $(SUBDIRS:.=$(DOMAIN).po) $(SUBDIRS:.=argparse.po)  ## Check for missing translations
> @for file in $^ \
; do \
echo $(MSGCMP) "$$file" "$$file" \
; $(MSGCMP) "$$file" "$$file" \
; if [ $$? -ne 0 ] \
; then \
exit 1 \
; fi \
; done

clean:  ## Clean up
> rm -f *.pot
> rm -f */LC_MESSAGES/*.mo
> rm -f */LC_MESSAGES/*.po~

help:  ## Display this help
> @$(AWK) 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
