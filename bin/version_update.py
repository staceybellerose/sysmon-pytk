#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2024 Stacey Adams <stacey.belle.rose@gmail.com>
# SPDX-License-Identifier: MIT

"""
Version updater.
"""

from __future__ import annotations

import argparse
import logging
import sys
from contextlib import suppress
from enum import IntEnum
from pathlib import Path

import coloredlogs
from packaging.version import Version
from redbaron import RedBaron

__version__ = "0.1"
logger = logging.getLogger(Path(__file__).name)


class UpgradeType(IntEnum):
    """
    Type of version update to do.
    """

    MAJOR = 1
    MINOR = 2
    PATCH = 3
    DEV = 4


def parse_cli_args() -> argparse.Namespace:
    """
    Parse the command line arguments.
    """
    app_desc = "Version Updater: update package version according to specified rules"
    epilog = "NOTE: Using -d will increment patch level if no update type specified."
    parser = argparse.ArgumentParser(description=app_desc, epilog=epilog)
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"Version Updater {__version__}",
        help="show program's version number and exit"
    )
    parser.add_argument(
        "-V", "--verbose", action="count", dest="verbose", default=0,
        help="give more output"
    )
    parser.add_argument(
        "-D", "--dry-run", action="store_true", dest="dryrun",
        help="only show what changes will be made; don't actually make them"
    )
    parser.add_argument(
        "-b", "--backup", action="store_true", dest="backup",
        help="back up FILE before writing the new version out (%%.py~)"
    )
    dev_options = parser.add_argument_group("dev release arguments")
    dev_type = dev_options.add_mutually_exclusive_group()
    dev_type.add_argument(
        "-a", "--add-dev", action="store_true", dest="dev",
        help="add a developmental release tag after updating the version"
    )
    dev_type.add_argument(
        "-r", "--remove-dev", action="store_true", dest="remove_dev",
        help="remove the developmental release tag from the version"
    )
    required_options = parser.add_argument_group("upgrade type arguments")
    update_type = required_options.add_mutually_exclusive_group()
    update_type.add_argument(
        "-m", "--major", action="store_const", dest="update", const=UpgradeType.MAJOR,
        help="update the major version"
    )
    update_type.add_argument(
        "-n", "--minor", action="store_const", dest="update", const=UpgradeType.MINOR,
        help="update the minor version"
    )
    update_type.add_argument(
        "-p", "--patch", action="store_const", dest="update", const=UpgradeType.PATCH,
        help="update the patch level"
    )
    update_type.add_argument(
        "-d", "--dev", action="store_const", dest="update", const=UpgradeType.DEV,
        help="update the developmental release level"
    )
    parser.add_argument(
        "file", metavar="FILE", type=argparse.FileType("rb"),
        help="name of python file containing __version__ definition"
    )
    return parser.parse_args()


def calc_new_version(
    version: Version, update: UpgradeType, *, add_dev: bool, remove_dev: bool
) -> Version:
    """
    Calculate the new version number.
    """
    converters = {
        UpgradeType.DEV: update_dev,
        UpgradeType.PATCH: update_patch,
        UpgradeType.MINOR: update_minor,
        UpgradeType.MAJOR: update_major
    }
    if update is None and add_dev:
        update = UpgradeType.PATCH
        logger.debug("no update type provided when adding dev tag; using PATCH")
    with suppress(KeyError):
        version = converters[update](version)
    if update != UpgradeType.DEV and add_dev:
        version = add_dev_tag(version)
    if remove_dev:
        version = remove_dev_tag(version)
    return version


def add_dev_tag(version: Version) -> Version:
    """
    Add a developmental release level to the current version number.
    """
    return Version(".".join(map(str, version.release))+".dev1")


def remove_dev_tag(version: Version) -> Version:
    """
    Remove the developmental release level from the current version number.
    """
    return Version(".".join(map(str, version.release)))


def update_dev(version: Version) -> Version:
    """
    Update the developmental release level.
    """
    dev = version.dev + 1 if version.dev is not None else 1
    return Version(".".join(map(str, version.release))+f".dev{dev}")


def update_patch(version: Version) -> Version:
    """
    Update the patch level.
    """
    major, minor, patch = version.release
    patch += 1
    return Version(".".join(map(str, [major, minor, patch])))


def update_minor(version: Version) -> Version:
    """
    Update the minor version number.
    """
    major, minor, patch = version.release
    minor += 1
    patch = 0
    return Version(".".join(map(str, [major, minor, patch])))


def update_major(version: Version) -> Version:
    """
    Update the major version number.
    """
    major, minor, patch = version.release
    major += 1
    minor = 0
    patch = 0
    return Version(".".join(map(str, [major, minor, patch])))


def process_file(cli_args: argparse.Namespace) -> None:
    """
    Process the python file passed in.
    """
    fname = cli_args.file.name
    with Path(fname).open(mode="r", encoding="UTF-8") as source_code:
        red = RedBaron(source_code.read())
    node = red.find("assignment", lambda node: node.target.name.value == "__version__")
    if node is None:
        msg = "__version__ assignment not found in source code"
        logger.error(msg)
        sys.exit(1)
    version = Version(str(node.value)[1:-1])  # strip the quotes used by Baron
    logger.info("Found version number: %s", version)
    new_version = calc_new_version(
        version, cli_args.update, add_dev=cli_args.dev, remove_dev=cli_args.remove_dev
    )
    logger.info("New version number: %s", new_version)
    node.value = f'"{new_version}"'
    if cli_args.dryrun:
        logger.info("Dry-run flag set. No files changed.")
        # logger.debug("\n%s", red.dumps())
        return
    formatted_code = red.dumps()
    if cli_args.backup:
        Path(fname).rename(f"{fname}~")
        logger.info("Backed up original file")
    with Path(fname).open(mode="w", encoding="UTF-8") as outfile:
        outfile.write(formatted_code)
        logger.info("Wrote updated file")


def get_logging_level(verbose: int) -> int:
    """
    Convert from command line argument "verbose" to logging level.
    """
    if verbose <= 0:
        return logging.INFO
    return logging.DEBUG


if __name__ == "__main__":
    args = parse_cli_args()
    coloredlogs.install(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        level=get_logging_level(args.verbose)
    )
    logger.debug(args)
    if args.update is None and not args.dev and not args.remove_dev:
        logger.warning("Nothing to do. Please use an option to indicate what to update.")
        sys.exit(1)
    process_file(args)
