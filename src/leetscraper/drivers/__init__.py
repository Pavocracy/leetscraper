# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""leetscraper currently supports chromedriver, geckodriver."""

__all__ = ["create_chromedriver", "create_geckodriver"]

from .chromedriver import create_chromedriver
from .geckodriver import create_geckodriver
