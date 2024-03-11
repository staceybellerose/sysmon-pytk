#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Read a toml file and print the value found at a given tree path.
"""

import argparse
import tomli


def _get_dict_entry(dc: dict, path: list):
    if len(path) == 1:
        return dc[path[0]]
    return _get_dict_entry(dc[path[0]], path[1:])


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "filename", metavar="filename", type=str, help="TOML filename to process"
)
parser.add_argument(
    "node", type=str, nargs="*", help="Tree node in TOML file"
)
args = parser.parse_args()
nodes = [int(arg) if arg.isdigit() else arg for arg in args.node]
with open(args.filename, "rb") as file:
    td = tomli.load(file)
    print(_get_dict_entry(td, nodes))
