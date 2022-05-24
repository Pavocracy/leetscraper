# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the utility functions to help gather information on the
system used and its avaliable programs, or other information gathered during
the scraping process."""

from os import getcwd, makedirs, path
from re import sub
from subprocess import run
from sys import platform
from time import perf_counter
from typing import Dict

from .logger import log_message


def check_exec_time(
        start_time: float,
        stop_time: float,
        funct_name: str) -> tuple:
    """Given two perf_counter times, compute the exec_time and return it and
    its unit of time.

    The funct_name of where this function was called from is also
    required for logging purposes.
    """
    time_units = [
        "seconds",
        "milliseconds",
        "microseconds",
        "nanoseconds",
        "picoseconds",
        "femtoseconds"]
    try:
        exec_time = stop_time - start_time
        for time_unit in time_units:
            if int(exec_time) != 0:
                return int(exec_time), time_unit
            exec_time *= 1000
        raise Exception("Reached end of loop without computing exec_time!")
    except Exception as error:
        message = f"Could not compute exec_time of {funct_name}! {error}"
        log_message("debug", message)
        return "unknown", "time"


def check_path(scrape_path: str) -> str:
    """Check if the given path can be used to scrape problems to."""
    log_message(
        "debug",
        "Checking if %s can be used for scrape_path",
        path.abspath(scrape_path))
    start = perf_counter()
    if not path.isdir(scrape_path):
        try:
            makedirs(scrape_path)
        except Exception as error:
            if scrape_path != getcwd():
                log_message(
                    "warning",
                    "Could not use path %s! %s. Trying %s instead!",
                    path.abspath(scrape_path),
                    error,
                    getcwd(),
                )
                scrape_path = getcwd()
                check_path(scrape_path)
            else:
                message = f"{scrape_path} Error!: {error}"
                log_message("exception", message)
                raise Exception(message) from error
    stop = perf_counter()
    exec_time, time_unit = check_exec_time(start, stop, "check_path")
    log_message(
        "debug",
        "Confirmed %s can be used in %s %s",
        scrape_path,
        exec_time,
        time_unit)
    return scrape_path


def check_platform() -> str:
    """Check which operating system is used for supported browser query.

    Raise an exception if the operating system is not supported.
    """
    log_message("debug", "Checking if %s is a supported OS", platform)
    user_platform = ""
    start = perf_counter()
    if platform.startswith("darwin"):
        user_platform = "mac"
    if platform.startswith("linux"):
        user_platform = "linux"
    if platform.startswith("win32"):
        user_platform = "windows"
    stop = perf_counter()
    exec_time, time_unit = check_exec_time(start, stop, "check_platform")
    if user_platform:
        log_message(
            "debug",
            "Confirmed %s is a supported OS in %s %s",
            user_platform,
            exec_time,
            time_unit)
        return user_platform
    message = "You are not using a supported OS!"
    log_message("exception", message)
    raise Exception(message)


def check_supported_browsers(user_platform: str) -> Dict[str, str]:
    """Looks for supported browsers installed to initialize the correct
    webdriver version.

    Raise an exception if no supported browsers found on the callers
    operating system.
    """
    log_message(
        "debug",
        "Checking for supported browsers installed on this system")
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
    start = perf_counter()
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
    stop = perf_counter()
    exec_time, time_unit = check_exec_time(
        start, stop, "check_supported_browsers")
    if avaliable_browsers:
        log_message(
            "debug",
            "Found browsers %s in %s %s",
            avaliable_browsers,
            exec_time,
            time_unit)
        return avaliable_browsers
    message = "No supported browser found!"
    log_message("exception", message)
    raise Exception(message)
