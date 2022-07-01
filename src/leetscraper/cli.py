#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the command-line interface for leetscraper."""

from argparse import ArgumentParser


__version__ = "2.3.0"
# fmt: off
leetscraper_logo=(
f"""
 __             __
|  |.----.-----|  |_.-----.----.----.---.-.-----.-----.----.
|  |  -__|  -__|   _|__ --|  __|   _|  _  |  _  |  -__|   _|
|__|_____|_____|____|_____|____|__| |___._|   __|_____|__|
         Copyright (C) 2022 Pavocracy     |__|  v{__version__}
"""
)
# fmt: on


def main():
    """Leetscrape cli."""
    # TODO: impliment cli
    parser = ArgumentParser(
        prog="leetscraper",
        usage="leetscraper [-flag] [OPTION]",
        description=leetscraper_logo,
        add_help=True,
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Print out leetscraper version",
        action="store_true",
    )

    args = parser.parse_args()

    if args.version:
        print(f"leetscraper v{__version__}")
        return

    print("cli not implemented yet!")


if __name__ == "__main__":
    main()
