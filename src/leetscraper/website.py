# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the function which is responsible for initializating
the required class for successful scraping of the given supported website."""

from time import perf_counter
from typing import Union

from .logger import log_message
from .utils import check_exec_time
from .websites import Codechef, Codewars, Hackerrank, Leetcode, Projecteuler


WebsiteType = Union[Codechef, Codewars, Hackerrank, Leetcode, Projecteuler]


def set_website(
    website_name: str,
) -> WebsiteType:
    """Return class object for a supported website.

    Raise an exception if website_name is not supported.
    """
    log_message("debug", "Initializing Leetscraper for %s", website_name)
    website = WebsiteType
    start = perf_counter()
    if "leetcode" in website_name.lower():
        website = Leetcode()
    elif "projecteuler" in website_name.lower():
        website = Projecteuler()
    elif "codechef" in website_name.lower():
        website = Codechef()
    elif "hackerrank" in website_name.lower():
        website = Hackerrank()
    elif "codewars" in website_name.lower():
        website = Codewars()
    else:
        message = f"{website_name} is not a supported website!"
        log_message("exception", message)
        raise Exception(message)
    stop = perf_counter()
    exec_time, time_unit = check_exec_time(start, stop, "set_website")
    log_message(
        "debug",
        "Initialized for %s in %s %s",
        website_name,
        exec_time,
        time_unit)
    return website  # type: ignore[return-value]
