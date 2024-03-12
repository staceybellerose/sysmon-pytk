# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

SHELL = /bin/bash

MSGMERGE = msgmerge
MSGFMT = msgfmt
XGETTEXT = xgettext
WIDTH = 79

# make sure all external programs are available
EXECUTABLES = xgettext msgfmt msgmerge awk touch
K := $(foreach exec,$(EXECUTABLES),\
    $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

DOMAIN = $(shell awk '$$0 ~ "^__i18n_domain__" { gsub(/"/, ""); print $$2 }' FS=" = " ../app_locale.py)
PACKAGE = $(shell awk '$$0 ~ "^__app_name__" { gsub(/"/, ""); print $$2 }' FS=" = " ../about.py)
VERSION = $(shell awk '$$0 ~ "^__version__" { gsub(/"/, ""); print $$2 }' FS=" = " ../about.py)
AUTHOR = $(shell awk '$$0 ~ "^__author_name__" { gsub(/"/, ""); print $$2 }' FS=" = " ../about.py)
AUTHOR_EMAIL = $(shell awk '$$0 ~ "^__author_email__" { gsub(/"/, ""); print $$2 }' FS=" = " ../about.py)
COPYRIGHT_HOLDER = $(AUTHOR) <$(AUTHOR_EMAIL)>
MSGID_BUGS_ADDRESS = $(AUTHOR_EMAIL)

SUBDIRS := $(wildcard */LC_MESSAGES/.)

.DEFAULT_GOAL := help

.PHONY: pot po mo clean help all

all: pot po mo  ## Regenerate all translation files

pot: $(DOMAIN).pot  ## Regenerate POT file

po: $(SUBDIRS:.=$(DOMAIN).po)  ## Update PO files

mo: $(SUBDIRS:.=$(DOMAIN).mo)  ## Compile MO files

$(DOMAIN).pot: ../*.py
	xgettext --default-domain="$(DOMAIN)" --output="$(DOMAIN).pot" --verbose \
	--add-location=full --width=$(WIDTH) --copyright-holder="$(COPYRIGHT_HOLDER)" \
	--package-name="$(PACKAGE)" --package-version="$(VERSION)" \
	--msgid-bugs-address="$(MSGID_BUGS_ADDRESS)" $^

define gen-po =
if [ -f "$@" ] \
; then \
	msgmerge --add-location=full --width=$(WIDTH) --update $@ $< \
; else \
	cp -v $< $@ \
; fi
@touch -d yesterday $(@D)/$(shell basename $(@) .po).mo
@touch $@
endef

%/LC_MESSAGES/$(DOMAIN).po: $(DOMAIN).pot
	$(gen-po)

%/LC_MESSAGES/$(DOMAIN).mo: %/LC_MESSAGES/$(DOMAIN).po
	msgfmt --verbose --output-file=$@ $<

clean:  ## Clean up
	rm -rf *.pot
	rm -f */LC_MESSAGES/*.mo
	rm -f */LC_MESSAGES/*.po~

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
