# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the Hackerrank class and its methods.
Initialisation of the class will set attributes required for most of
the class methods. Some Leetscraper attributes will be required.
"""

from json import loads
from typing import List, Optional

from urllib3 import PoolManager

from ..logger import get_logger
from ..system import check_platform, check_supported_browsers


class Hackerrank:
    """This class contains the methods required to scrape problems for hackerrank.com."""

    def __init__(self):
        """These are the attributes specific to URLs and HTML tags for hackerrank.com."""
        # TODO: Handle multiple HTML tags when a website is not consistent?
        self.website_name = "hackerrank.com"
        self.categories = ["algorithms", "data-structures", "mathematics", "ai", "fp"]
        self.api_url = "https://www.hackerrank.com/rest/contests/master/tracks/"
        self.base_url = "https://www.hackerrank.com/challenges/"
        self.problem_description = {"class": "problem-statement"}
        self.file_split = "."
        # Hackerrank requires User-Agent headers for scraping.
        platform = check_platform()
        self.browsers = check_supported_browsers(platform)

    def get_problems(
        self, http: PoolManager, scraped_problems: List[str], scrape_limit: int
    ) -> List[List[Optional[str]]]:
        """Returns problems to scrape defined by checks in this method."""
        get_problems = []
        try:
            headers = {}
            browser, version = list(self.browsers.items())[0]
            headers["User-Agent"] = f"{browser}/{version}"
            for category in self.categories:
                for i in range(0, 1001, 50):
                    request = http.request(
                        "GET",
                        self.api_url + category + f"/challenges?offset={i}&limit=50",
                        headers=headers,
                    )
                    data = loads(request.data.decode("utf-8"))
                    if data["models"]:
                        for problem in data["models"]:
                            if problem["slug"] not in scraped_problems:
                                get_problems.append(
                                    [
                                        problem["slug"] + "/problem",
                                        problem["difficulty_name"].upper(),
                                    ]
                                )
                                if (
                                    scrape_limit > 0
                                    and len(get_problems) >= scrape_limit
                                ):
                                    return get_problems
                    else:
                        break
        except Exception as error:
            logger = get_logger()
            logger.warning(
                "Failed to get problems for %s. Error: %s", self.website_name, error
            )
        return get_problems

    def filter_problem(
        self,
        soup: str,
        problem: List[str],
    ) -> tuple:
        """Filters the soup html down to the problem description using HTML tags.\n
        Sets the problem_name, and problem_difficulty if needed.\n
        If an Error happens, it will return the error message instead.
        """
        try:
            problem_description = (
                soup.find("div", self.problem_description).get_text().strip()
            )
            problem_name = problem[0].split("/")[0]
        except Exception as error:
            return "Error!", error, problem
        return problem_name, problem_description, problem
