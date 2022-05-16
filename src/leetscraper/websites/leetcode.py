# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the Leetcode class and its methods. Initialisation of the class will set
attributes required for most of the class methods. Some Leetscraper attributes will be required.
"""

from json import loads
from typing import List, Optional

from urllib3 import PoolManager

from ..logger import log_message


class Leetcode:
    """This class contains the methods required to scrape problems for leetcode.com."""

    def __init__(self):
        """These are the attributes specific to URLs and HTML tags for leetcode.com."""
        self.website_name = "leetcode.com"
        self.difficulty = {1: "EASY", 2: "MEDIUM", 3: "HARD"}
        self.api_url = "https://leetcode.com/api/problems/all/"
        self.base_url = "https://leetcode.com/problems/"
        self.problem_description = {"class": "content__u3I1 question-content__JfgR"}
        self.file_split = "."
        # leetcode seems to block requests when using custom headers :(
        self.need_headers = False

    def get_problems(
        self, http: PoolManager, scraped_problems: List[str], scrape_limit: int
    ) -> List[List[Optional[str]]]:
        """Returns problems to scrape defined by checks in this method."""
        try:
            get_problems: list = []
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
            log_message(
                "warning",
                "Failed to get problems for %s. Error: %s",
                self.website_name,
                error,
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
