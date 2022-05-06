# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the functions which are responsible for
checking if the operating system used is supported, if the given
path is valid, and looks for a supported browser to use for the WebDriver.
"""

from os import path, makedirs, getcwd
from re import sub
from sys import platform
from subprocess import run
from typing import Dict

from .logger import get_logger


def check_path(scrape_path: str) -> str:
    """Check if the given path can be used to scrape problems to."""
    if not path.isdir(scrape_path):
        try:
            makedirs(scrape_path)
        except Exception as error:
            if scrape_path != getcwd():
                logger = get_logger()
                logger.warning(
                    "Could not use path %s! %s. Trying %s instead!",
                    scrape_path,
                    error,
                    getcwd(),
                )
                check_path(getcwd())
            else:
                message = f"{scrape_path} Error!: {error}"
                logger = get_logger()
                logger.exception(message)
                raise Exception(message) from error
    return scrape_path


def check_platform() -> str:
    """Check which operating system is used for supported browser query.
    Raise an exception if the operating system is not supported.
    """
    if platform.startswith("darwin"):
        return "mac"
    if platform.startswith("linux"):
        return "linux"
    if platform.startswith("win32"):
        return "windows"
    message = "You are not using a supported OS!"
    logger = get_logger()
    logger.exception(message)
    raise Exception(message)


def check_supported_browsers(user_platform: str) -> Dict[str, str]:
    """Looks for supported browsers installed to initialize the correct webdriver version.
    Raise an exception if no supported browsers found on the callers operating system.
    """
    avaliable_browsers = {}
    query = {
        "chrome": {
            "mac": "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version",
            "linux": "google-chrome --version",
            "windows": 'powershell -command "&{(Get-Item C:\\Program` Files\\Google\\Chrome\\Application\\chrome.exe).VersionInfo.ProductVersion}"',
        },
        "firefox": {
            "mac": "/Applications/Firefox.app/Contents/MacOS/firefox -v",
            "linux": "firefox --version",
            "windows": '"C:\\Program Files\\Mozilla Firefox\\firefox.exe" -v | more',
        },
    }
    for browser, operating_system in query.items():
        try:
            check_browser_version = run(
                operating_system[user_platform],
                capture_output=True,
                check=True,
                shell=True,
            )
            get_version = str(check_browser_version.stdout)
            browser_version = sub("[^0-9.]+", "", get_version)
            avaliable_browsers[browser] = browser_version
        except Exception:
            message = f"Could not find {browser} version! checking for other browsers"
            logger = get_logger()
            logger.warning(message)
    if avaliable_browsers:
        return avaliable_browsers
    message = "No supported browser found!"
    logger = get_logger()
    logger.exception(message)
    raise Exception(message)
