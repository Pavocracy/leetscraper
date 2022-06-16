# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the function to create a chromedriver."""

from os import devnull

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_chromedriver(
        webdriver_version: str,
        user_agent: str) -> webdriver.Chrome:
    """Create and return the correct version of the webdriver."""
    service = Service(
        ChromeDriverManager(
            version=webdriver_version,
            log_level=0,
            print_first_line=False,
        ).install(),
        log_path=devnull,
    )
    options = Options()
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    if user_agent:
        options.add_argument(f"--user-agent={user_agent}")
    driver = webdriver.Chrome(
        service=service, options=options)
    return driver
