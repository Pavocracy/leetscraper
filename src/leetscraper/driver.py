# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the functions which are responsible for installing the
correct version of the webdriver for the supported browser being used, and
closing the webdriver."""

from datetime import date
from json import load
from os import devnull, environ, path
from time import perf_counter
from typing import Dict, Union

from selenium import webdriver

from .logger import log_message
from .utils import check_exec_time
from .website import WebsiteType

WebdriverType = Union[webdriver.Firefox, webdriver.Chrome]


def check_installed_webdrivers() -> Dict[str, str]:
    """Checks for installed webdrivers to use.

    Will only use webdrivers cached today.
    """
    # Much of the code in this function mirrors the patterns found in webdriver_manager.
    # https://github.com/SergeyPirogov/webdriver_manager/blob/master/webdriver_manager/driver_cache.py
    log_message("debug", "Checking for any cached webdrivers to use")
    installed_webdrivers: dict = {}
    try:
        start = perf_counter()
        # This is to match the date format wdm uses.
        today = date.today().strftime("%d/%m/%Y")
        # This is the default path where wdm stores the list of cached
        # webdrivers.
        wdm_drivers = path.join(path.expanduser("~"), ".wdm", "drivers.json")
        with open(wdm_drivers, "r", encoding="utf-8") as file:
            cached_webdrivers = load(file)
            for found_webdriver in cached_webdrivers:
                timestamp = cached_webdrivers[found_webdriver]["timestamp"]
                if timestamp == today:
                    cached_webdriver = found_webdriver.split("_")[1]
                    cached_webdriver_version = found_webdriver.split("_")[2]
                    other_webdrivers = installed_webdrivers.get(
                        cached_webdriver, None)
                    if other_webdrivers:
                        # Remove v from driver version and compare versions as
                        # a tuple of ints.
                        current = tuple(
                            map(
                                int,
                                (other_webdrivers.replace("v", "").split(".")),
                            )
                        )
                        new = tuple(
                            map(
                                int,
                                (cached_webdriver_version.replace("v", "").split(".")),
                            )
                        )
                        if new > current:
                            installed_webdrivers[
                                cached_webdriver
                            ] = cached_webdriver_version
                    installed_webdrivers[cached_webdriver] = cached_webdriver_version
        if not installed_webdrivers:
            raise Exception
    except Exception:
        log_message(
            "debug",
            "Did not find any recent webdrivers! Will download the latest drivers instead.",
        )
        return installed_webdrivers
    stop = perf_counter()
    exec_time, time_unit = check_exec_time(
        start, stop, "check_installed_webdrivers")
    log_message("debug", "Found cached webdrivers %s in %s %s",
                installed_webdrivers, exec_time, time_unit)
    return installed_webdrivers


def header_constructor(
    leetscraper_version: str, browser: str, browser_version: str
) -> str:
    """Construct custom user-agent header to try and do the right thing by
    letting these websites know this is a bot making requests to their
    servers."""
    return f"Mozilla/5.0 (compatible; Leetscraper/{leetscraper_version}; +https://github.com/Pavocracy/leetscraper) {browser}/{browser_version}"


def create_webdriver(
    avaliable_browsers: dict,
    website: WebsiteType,
    installed_webdrivers: dict,
    leetscraper_version: str,
) -> WebdriverType:
    """Initializes the webdriver with pre-defined options."""
    # This is a current workaround for a bug that can cause the webdriver to
    # stall for 5 minutes during the initial webpage opening.
    # This is a very well known issue. See the issue card for details.
    # https://github.com/Pavocracy/leetscraper/issues/67
    environ["DBUS_SESSION_BUS_ADDRESS"] = devnull
    for browser, browser_version in avaliable_browsers.items():
        log_message(
            "debug",
            "Attempting to initialize the webdriver for %s v%s",
            browser,
            browser_version)
        try:
            user_agent: str = ""
            if website.need_headers:
                user_agent = header_constructor(
                    leetscraper_version, browser, browser_version
                )
            start = perf_counter()
            if browser == "chrome":
                from selenium.webdriver.chrome.service import (
                    Service as ChromeService,
                )
                from selenium.webdriver.chrome.options import (
                    Options as ChromeOptions,
                )
                from webdriver_manager.chrome import ChromeDriverManager

                webdriver_version = installed_webdrivers.get(
                    "chromedriver", "latest")
                service = ChromeService(
                    ChromeDriverManager(
                        version=webdriver_version,
                        log_level=0,
                        print_first_line=False,
                    ).install(),
                    log_path=devnull,
                )
                options = ChromeOptions()
                options.add_experimental_option(
                    "excludeSwitches", ["enable-logging"])
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                if user_agent:
                    options.add_argument(f"--user-agent={user_agent}")
                driver = webdriver.Chrome(
                    service=service, options=options)
            if browser == "firefox":
                from selenium.webdriver.firefox.service import (
                    Service as FirefoxService,
                )
                from selenium.webdriver.firefox.options import (
                    Options as FirefoxOptions,
                )
                from webdriver_manager.firefox import GeckoDriverManager

                webdriver_version = installed_webdrivers.get(
                    "geckodriver", "latest")
                service = FirefoxService(
                    GeckoDriverManager(
                        version=webdriver_version,
                        log_level=0,
                        print_first_line=False,
                    ).install(),
                    log_path=devnull,
                )
                options = FirefoxOptions()
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
            driver.implicitly_wait(0)
            stop = perf_counter()
            exec_time, time_unit = check_exec_time(
                start, stop, "create_webdriver")
            log_message(
                "debug",
                "Initialized %s webdriver %s in %s %s",
                driver.name,
                webdriver_version,
                exec_time,
                time_unit,
            )
            return driver
        except Exception as error:
            log_message(
                "warning",
                "Could not initialize %s! %s. Trying another browser!",
                browser,
                error,
            )
    message = "Could not initialize any browsers found!"
    log_message("exception", message)
    raise Exception(message)


def webdriver_quit(
    driver: WebdriverType,
    website_name: str,
):
    """Closes the webdriver."""
    try:
        start = perf_counter()
        driver.quit()
        stop = perf_counter()
        exec_time, time_unit = check_exec_time(start, stop, "webdriver_quit")
        log_message(
            "debug",
            "Closed %s webdriver used for %s in %s %s",
            driver.name,
            website_name,
            exec_time,
            time_unit,
        )
    except Exception as error:
        log_message("exception", error)
