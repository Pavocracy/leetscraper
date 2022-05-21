# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the function which is responsible for initializating
the required class for successful scraping of the given supported website."""

from typing import Union

from .logger import log_message
from .websites import Codechef, Codewars, Hackerrank, Leetcode, Projecteuler


WebsiteType = Union[Codechef, Codewars, Hackerrank, Leetcode, Projecteuler]


def set_website(
    website_name: str,
) -> WebsiteType:
    """Return class object for a supported website.

    Raise an exception if website_name is not supported.
    """
    log_message("debug", "Attempting to initialize for %s", website_name)
    if "leetcode" in website_name.lower():
        return Leetcode()
    if "projecteuler" in website_name.lower():
        return Projecteuler()
    if "codechef" in website_name.lower():
        return Codechef()
    if "hackerrank" in website_name.lower():
        return Hackerrank()
    if "codewars" in website_name.lower():
        return Codewars()
    message = f"{website_name} is not a supported website!"
    log_message("exception", message)
    raise Exception(message)
