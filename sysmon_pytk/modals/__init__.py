# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Modal dialogs.
"""

from .about_modal import AboutDialog
from .cpu_modal import CpuDialog
from .disk_usage_modal import DiskUsageDialog
from .font_modal import FontChooser
from .mem_usage_modal import MemUsageDialog
from .settings_modal import SettingsDialog
from .temperature_modal import TempDetailsDialog

__all__ = [
    "AboutDialog",
    "CpuDialog",
    "DiskUsageDialog",
    "FontChooser",
    "MemUsageDialog",
    "SettingsDialog",
    "TempDetailsDialog"
]
