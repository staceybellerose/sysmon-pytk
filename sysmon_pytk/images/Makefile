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
CONVERT := /usr/bin/convert
OPTIPNG := /usr/bin/optipng

# make sure all external programs are available
EXECUTABLES = $(CONVERT) $(OPTIPNG) $(AWK)
K := $(foreach exec,$(EXECUTABLES), $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.DEFAULT_GOAL := help

.PHONY: all clean clean-all help custom

work_action_icons := work/edit-copy.png work/edit-cut.png work/edit-paste.png work/edit-select-all.png work/view-refresh.png
work_app_icons := work/internet-group-chat.png
work_app_icons_32 := work/utilities-system-monitor.png
work_app_icons_scalable := work/utilities-system-monitor.svg
work_category_icons := work/preferences-system.png

app_icons = icon.png icon-lg.png
context_icons = edit-copy.png edit-cut.png edit-paste.png edit-select-all.png
main_menu_icons = blank.png preferences-system.png view-refresh.png internet-group-chat.png
custom_icons = custom/dialog-error.png custom/dialog-information.png custom/dialog-warning.png custom/dialog-question.png

define add-border =
$(CONVERT) -compose Copy -border 2x1 -bordercolor none $@ $@
endef

define optimize =
$(OPTIPNG) -strip all -o7 $@
endef

##@ Processing

all: $(app_icons) $(context_icons) $(main_menu_icons) $(custom_icons)  ## Extract and process all images

work:
> mkdir -p work

custom: $(custom_icons)

%.png : work/%.png
> cp $< $@
> $(optimize)

custom/%.png : custom/%.svg
> convert -background none -density 1200 -resize 96x96 $< $<.png
> mv $<.png $@
> $(optimize)

blank.png:
> convert -size 22x22 xc:transparent blank.png
> $(add-border)
> $(optimize)

icon.png: work/utilities-system-monitor.png
> cp $< $@
> $(optimize)

icon-lg.png: work/utilities-system-monitor.svg
> convert -background none -density 1200 -resize 96x96 $< $<.png
> cp $<.png $@
> $(optimize)

$(work_action_icons): | work
> tar -xzf tango-icon-theme-0.8.90.tar.gz -C work --xform='s|.*/||' tango-icon-theme-0.8.90/22x22/actions/$(subst work/,,$@)
> $(add-border)

$(work_app_icons): | work
> tar -xzf tango-icon-theme-0.8.90.tar.gz -C work --xform='s|.*/||' tango-icon-theme-0.8.90/22x22/apps/$(subst work/,,$@)
> $(add-border)

$(work_app_icons_32): | work
> tar -xzf tango-icon-theme-0.8.90.tar.gz -C work --xform='s|.*/||' tango-icon-theme-0.8.90/32x32/apps/$(subst work/,,$@)

$(work_app_icons_scalable): | work
> tar -xzf tango-icon-theme-0.8.90.tar.gz -C work --xform='s|.*/||' tango-icon-theme-0.8.90/scalable/apps/$(subst work/,,$@)

$(work_category_icons): | work
> tar -xzf tango-icon-theme-0.8.90.tar.gz -C work --xform='s|.*/||' tango-icon-theme-0.8.90/22x22/categories/$(subst work/,,$@)
> $(add-border)

##@ Cleanup

clean:  ## Clean up the folder
> rm -rf work

clean-all: clean  ## Deep clean the image folder (remove images)
> rm -f *.png
> rm -f custom/*.png

##@ Helpers

help:  ## Display this help
> @$(AWK) 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
