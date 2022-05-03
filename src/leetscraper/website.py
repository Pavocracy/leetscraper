# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the function which is responsible for
initializating the required class for successful scraping of the
given supported website.
"""

from .leetcode import Leetcode
from .logger import get_logger

# from .projecteuler import Projecteuler
# from .codechef import Codechef
# from .hackerrank import Hackerrank
# from .codewars import Codewars

# websiteType = Union[Leetcode, Projecteuler, Codechef, Hackerrank, Codewars]


def set_website(
    website_name: str,
) -> Leetcode:  # websiteType:
    """Return class object for a supported website.
    Raise an exception if website_name is not supported.
    """
    if website_name == "leetcode.com":
        return Leetcode()
    message = f"{website_name} is not a supported website!"
    logger = get_logger()
    logger.exception(message)
    raise Exception(message)
    """
    if website_name == "leetcode.com":
        return Leetcode()
    elif website_name == "projecteuler.net":
        return {
            "difficulty": {33: "EASY", 66: "MEDIUM", 100: "HARD"},
            "api_url": "https://projecteuler.net/recent",
            "base_url": "https://projecteuler.net/problem=",
            "problem_description": {"id": "content"},
        }
    elif website_name == "codechef.com":
        return {
            "difficulty": {1: "SCHOOL", 2: "EASY", 3: "MEDIUM", 4: "HARD"},
            "api_url": "https://www.codechef.com/api/list/problems/",
            "base_url": "https://www.codechef.com/problems/",
            "problem_description": {"class": "problem-statement"},
        }
    elif website_name == "hackerrank.com":
        return {
            "categories": [
                "algorithms",
                "data-structures",
                "mathematics",
                "ai",
                "fp",
            ],
            "api_url": "https://www.hackerrank.com/rest/contests/master/tracks/",
            "base_url": "https://www.hackerrank.com/challenges/",
            "problem_description": {"class": "problem-statement"},
        }
    elif website_name == "codewars.com":
        return {
            "difficulty": {
                8: "EASY",
                7: "EASY",
                6: "MEDIUM",
                5: "MEDIUM",
                4: "HARD",
                3: "HARD",
                2: "EXPERT",
                1: "EXPERT",
            },
            "api_url": "https://www.codewars.com/api/v1/code-challenges/",
            "base_url": "https://www.codewars.com/kata/",
            "problem_description": {"id": "description"},
        }
    else:
        message = f"{website_name} is not a supported website!"
        logging.exception(message)
        raise Exception(message)
    """
