# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the Codechef class and its methods.
Initialisation of the class will set attributes required for most of
the class methods. Some Leetscraper attributes will be required.
"""

from json import loads
from re import sub
from typing import List

from urllib3 import PoolManager

from src.leetscraper.logger import get_logger


class Codechef:
    """This class contains the methods required to scrape problems for codechef.com."""

    def __init__(self):
        """These are the attributes specific to URLs and HTML tags for codechef.com."""
        # TODO: Handle multiple HTML tags when a website is not consistent?
        self.website_name = "codechef.com"
        self.difficulty = {1: "SCHOOL", 2: "EASY", 3: "MEDIUM", 4: "HARD"}
        self.api_url = "https://www.codechef.com/api/list/problems/"
        self.base_url = "https://www.codechef.com/problems/"
        self.problem_description = {"class": "problem-statement"}
        self.file_split = "-"

    def get_problems(
        self, http: PoolManager, scraped_problems: List[str], scrape_limit: int
    ) -> List[List[str]]:
        """Returns problems to scrape defined by checks in this method."""
        get_problems = []
        try:
            for value in self.difficulty.values():
                request = http.request(
                    "GET",
                    self.api_url + value.lower() + "?limit=999",
                )
                data = loads(request.data.decode("utf-8"))
                for problem in data["data"]:
                    if problem["code"] not in scraped_problems:
                        get_problems.append([problem["code"], value])
                        if scrape_limit > 0 and len(get_problems) >= scrape_limit:
                            return get_problems
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
                soup.find("div", self.problem_description)
                .get_text()
                .split("Author:")[0]
                .strip()
            )
            get_name = (
                str(soup.find("aside", {"class": "breadcrumbs"}))
                .rsplit("»", maxsplit=1)[-1]
                .split("</")[0]
                .strip()
                .replace(" ", "-")
            )
            problem_name = sub("[^A-Za-z0-9-]+", "", get_name)
            problem_name = problem[0] + f"-{problem_name}"
        except Exception as error:
            return "Error!", error, problem
        return problem_name, problem_description, problem
