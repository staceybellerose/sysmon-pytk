#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Make script for pdoc documentation.
"""

from pathlib import Path

from pdoc import doc_types, pdoc, render
from pdoc._compat import formatannotation

from sysmon_pytk.font_utils import FontSlant, FontWeight

doc_types.simplify_annotation.replacements[
    formatannotation(FontSlant)
] = "sysmon_pytk.font_utils.FontSlant"
doc_types.simplify_annotation.replacements[
    formatannotation(FontWeight)
] = "sysmon_pytk.font_utils.FontWeight"
doc_types.simplify_annotation.replacements[
    formatannotation(tuple[FontWeight, FontSlant])
] = "tuple[sysmon_pytk.font_utils.FontWeight, sysmon_pytk.font_utils.FontSlant]"

doc_types.simplify_annotation.recompile()

here = Path(__file__).parent

render.configure(
    docformat="numpy",
    include_undocumented=False,
    favicon="https://raw.githubusercontent.com/staceybellerose/sysmon-pytk"
        "/main/sysmon_pytk/images/icon.png",
    template_directory=here / "_templates",
    edit_url_map={
        "sysmon_pytk":
            "https://github.com/staceybellerose/sysmon-pytk/blob/main/sysmon_pytk/",
        "azure":
            "https://github.com/staceybellerose/Azure-ttk-theme/blob/main/",
    }
)

# pdoc(here / ".." / "sysmon_pytk", output_directory=here / "build")
pdoc(here / ".." / "sysmon_pytk", here / ".." / "azure", output_directory=here / "build")
