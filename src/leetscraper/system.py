# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the functions which are responsible for checking if the operating system
used is supported, if the given path is valid, and looks for a supported browser to use for the
WebDriver.
"""

from os import getcwd, makedirs, path
from re import sub
from subprocess import run
from sys import platform
from typing import Dict

from .logger import log_message


def check_path(scrape_path: str) -> str:
    """Check if the given path can be used to scrape problems to."""
    if not path.isdir(scrape_path):
        try:
            makedirs(scrape_path)
        except Exception as error:
            if scrape_path != getcwd():
                log_message(
                    "warning",
                    "Could not use path %s! %s. Trying %s instead!",
                    scrape_path,
                    error,
                    getcwd(),
                )
                scrape_path = getcwd()
                check_path(scrape_path)
            else:
                message = f"{scrape_path} Error!: {error}"
                log_message("exception", message)
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
    log_message("exception", message)
    raise Exception(message)


def check_supported_browsers(user_platform: str) -> Dict[str, str]:
    """Looks for supported browsers installed to initialize the correct webdriver version.
    Raise an exception if no supported browsers found on the callers operating system.
    """
    # Much of the code in this function mirrors the patterns found in webdriver_manager.
    # https://github.com/SergeyPirogov/webdriver_manager/blob/master/webdriver_manager/utils.py
    avaliable_browsers: dict = {}
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
            log_message("warning", message)
    if avaliable_browsers:
        return avaliable_browsers
    message = "No supported browser found!"
    log_message("exception", message)
    raise Exception(message)
