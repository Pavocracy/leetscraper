# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the Leetcode class and its methods.
Initialisation of the class will set attributes required for most of
the class methods. Some Leetscraper attributes will be required.
"""

from json import loads
from typing import List

from urllib3 import PoolManager

from src.leetscraper.logger import get_logger


class Leetcode:
    """This class contains the methods required to scrape problems for leetcode.com."""

    def __init__(self):
        """These are the attributes specific to URLs and HTML tags for leetcode.com."""
        # TODO: Handle multiple HTML tags when a website is not consistent?
        self.website_name = "leetcode.com"
        self.difficulty = {1: "EASY", 2: "MEDIUM", 3: "HARD"}
        self.api_url = "https://leetcode.com/api/problems/all/"
        self.base_url = "https://leetcode.com/problems/"
        self.problem_description = {"class": "content__u3I1 question-content__JfgR"}
        self.file_split = "."

    def get_problems(
        self, http: PoolManager, scraped_problems: List[str], scrape_limit: int
    ) -> List[List[str]]:
        """Returns problems to scrape defined by checks in this method."""
        get_problems = []
        try:
            request = http.request("GET", self.api_url)
            data = loads(request.data.decode("utf-8"))
            for problem in data["stat_status_pairs"]:
                if (
                    problem["stat"]["question__title_slug"] not in scraped_problems
                    and problem["paid_only"] is not True
                ):
                    get_problems.append(
                        [
                            problem["stat"]["question__title_slug"],
                            self.difficulty[problem["difficulty"]["level"]],
                        ]
                    )
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
                soup.find("div", self.problem_description).get_text().strip()
            )
            problem_name = problem[0]
        except Exception as error:
            return "Error!", error, problem
        return problem_name, problem_description, problem
