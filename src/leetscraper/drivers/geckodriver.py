# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the function to create a geckodriver."""

from os import devnull

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager


def create_geckodriver(
        webdriver_version: str,
        user_agent: str) -> webdriver.Firefox:
    """Create and return the requested version of the webdriver."""
    service = Service(
        GeckoDriverManager(
            version=webdriver_version,
            log_level=0,
            print_first_line=False,
        ).install(),
        log_path=devnull,
    )
    options = Options()
    # Firefox does not allow no logging, So set to highest level
    # instead.
    options.set_capability(
        "moz:firefoxOptions", {"log": {"level": "fatal"}}
    )
    options.add_argument("-headless")
    if user_agent:
        options.set_preference(
            "general.useragent.override", user_agent)
    driver = webdriver.Firefox(
        service=service, options=options
    )
    return driver
