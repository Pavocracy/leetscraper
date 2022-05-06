# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the function which is responsible for
initializating the required class for successful scraping of the
given supported website.
"""

from typing import Union

from src.websites import Codechef, Codewars, Hackerrank, Leetcode, Projecteuler
from .logger import get_logger


WebsiteType = Union[Codechef, Codewars, Hackerrank, Leetcode, Projecteuler]


def set_website(
    website_name: str,
) -> WebsiteType:
    """Return class object for a supported website.
    Raise an exception if website_name is not supported.
    """
    if website_name == "leetcode.com":
        return Leetcode()
    if website_name == "projecteuler.net":
        return Projecteuler()
    if website_name == "codechef.com":
        return Codechef()
    if website_name == "hackerrank.com":
        return Hackerrank()
    if website_name == "codewars.com":
        return Codewars()
    logger = get_logger()
    message = f"{website_name} is not a supported website!"
    logger.exception(message)
    raise Exception(message)
