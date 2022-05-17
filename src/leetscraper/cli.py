#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the command-line interface for leetscraper."""

import argparse


def main():
    """Leetscrape cli"""
    # TODO: impliment cli
    parser = argparse.ArgumentParser(
        prog="leetscraper",
        usage="leetscraper [-flag] [OPTION]",
        description="Leetscraper cli",
        add_help=True,
    )
    parser.add_argument("-p", "--print", help="Print out given input")

    args = parser.parse_args()

    if args.print:
        print(f"args given! {args.print}")
    else:
        print("cli not implemented yet!")


if __name__ == "__main__":
    main()
