#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the command-line interface for leetscraper."""

from argparse import ArgumentParser, HelpFormatter

from textwrap import dedent, fill

from .version import check_version


class RawFormatter(HelpFormatter):
    def _fill_text(self, text, width, indent):
        # Strip the indent from the original python definition that plagues
        # most of us.
        text = dedent(text)
        text = indent(text, indent)  # Apply any requested indent.
        text = text.splitlines()  # Make a list of lines
        text = [fill(line, width) for line in text]  # Wrap each line
        text = "\n".join(text)  # Join the lines again
        return text


def main():
    """Leetscrape cli"""
    # TODO: impliment cli
    # fmt: off
    leetscraper="""
 __             __
|  .-----.-----|  |_.-----.----.----.---.-.-----.-----.----.
|  |  -__|  -__|   _|__ --|  __|   _|  _  |  _  |  -__|   _|
|__|_____|_____|____|_____|____|__| |___._|   __|_____|__|
                                          |__|""",
    # fmt: on
    parser = ArgumentParser(
        prog="leetscraper",
        usage="leetscraper [-flag] [OPTION]",
        description=leetscraper,
        formatter_class=RawFormatter,
        add_help=True,
    )
    parser.add_argument("-p", "--print", help="Print out given input")
    parser.add_argument(
        "-v",
        "--version",
        help="Print out leetscraper version",
        action="store_true",
    )

    args = parser.parse_args()

    if args.print:
        print(f"args given! {args.print}")
    if args.version:
        print(f"leetscraper v{check_version()}")
        return
    else:
        print("cli not implemented yet!")


if __name__ == "__main__":
    main()
