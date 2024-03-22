# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

from typing import Protocol

class GettextCallable(Protocol):
    def __call__(self, message: str) -> str: ...
