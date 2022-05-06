# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the functions which are responsible for
installing the correct version of the webdriver for the supported
browser being used, and closing the webdriver.
"""

from os import devnull
from typing import Union

from selenium import webdriver

from .logger import get_logger

WebdriverType = Union[webdriver.Firefox, webdriver.Chrome]


def create_webdriver(avaliable_browsers: dict, website_name: str) -> WebdriverType:
    """Initializes the webdriver with pre-defined options."""
    for browser, browser_version in avaliable_browsers.items():
        try:
            if browser == "chrome":
                from selenium.webdriver.chrome.service import Service as ChromeService
                from selenium.webdriver.chrome.options import Options as ChromeOptions
                from webdriver_manager.chrome import ChromeDriverManager

                service = ChromeService(
                    ChromeDriverManager(log_level=0, print_first_line=False).install(),
                    log_path=devnull,
                )
                options = ChromeOptions()
                options.add_experimental_option("excludeSwitches", ["enable-logging"])
                options.add_argument("--headless")
                options.add_argument("--silent")
                options.add_argument("--disable-gpu")
                if website_name == "hackerrank.com":
                    options.add_argument(f"user-agent={browser}/{browser_version}")
                driver = webdriver.Chrome(service=service, options=options)
            if browser == "firefox":
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                from webdriver_manager.firefox import GeckoDriverManager

                service = FirefoxService(
                    GeckoDriverManager(log_level=0, print_first_line=False).install(),
                    log_path=devnull,
                )
                options = FirefoxOptions()
                options.set_capability(
                    "moz:firefoxOptions", {"log": {"level": "fatal"}}
                )
                options.add_argument("--headless")
                # options.add_argument("--silent") no longer works since firefox 91.9.0esr?
                options.add_argument("--disable-gpu")
                driver = webdriver.Firefox(service=service, options=options)
            driver.implicitly_wait(0)
            logger = get_logger()
            logger.debug("Created %s webdriver for %s", driver.name, website_name)
            return driver
        except Exception as error:
            logger = get_logger()
            logger.warning(
                "Could not initialize %s! %s. Trying another browser!",
                browser,
                error,
            )
    message = "Could not initialize any browsers found!"
    logger = get_logger()
    logger.exception(message)
    raise Exception(message)


def webdriver_quit(
    driver: WebdriverType,
    website_name: str,
):
    """Closes the webdriver."""
    logger = get_logger()
    logger.debug("Closing %s driver", website_name)
    driver.quit()
