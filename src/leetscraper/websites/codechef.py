# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the Codechef class and its methods. Initialisation of the class will set
attributes required for most of the class methods. Some Leetscraper attributes will be required.
"""

from json import loads
from re import sub
from typing import List, Optional

from urllib3 import PoolManager

from ..logger import log_message


class Codechef:
    """This class contains the methods required to scrape problems for codechef.com."""

    def __init__(self):
        """These are the attributes specific to URLs and HTML tags for codechef.com."""
        self.website_name = "codechef.com"
        # Difficulty ratings based on https://blog.codechef.com/2022/02/25/exciting-updates-for-february-2022/
        self.difficulty = {
            "BEGINNER": 1000,
            "LEVEL 1": 1400,
            "LEVEL 2": 1600,
            "LEVEL 3": 1800,
            "LEVEL 4": 2000,
            "LEVEL 5": 2200,
            "LEVEL 6": 2500,
            "LEVEL 7": 9999,
        }
        self.api_url = "https://www.codechef.com/api/list/problems/"
        self.base_url = "https://www.codechef.com/problems/"
        # TODO: Handle multiple HTML tags needed for the problems that currently fail?
        self.problem_description = {"class": "problem-statement"}
        self.file_split = "-"
        self.need_headers = True

    def get_problems(
        self, http: PoolManager, scraped_problems: List[str], scrape_limit: int
    ) -> List[List[Optional[str]]]:
        """Returns problems to scrape defined by checks in this method."""
        try:
            get_problems: list = []
            headers: dict = {}
            headers["User-Agent"] = self.headers
            request = http.request(
                "GET", self.api_url + "?limit=99999", headers=headers
            )
            data = loads(request.data.decode("utf-8"))
            for problem in data["data"]:
                if problem["code"] not in scraped_problems:
                    get_problems.append([problem["code"], None])
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
            filter_problem = (
                soup.find("div", self.problem_description).get_text().strip()
            )
            problem_description = filter_problem.split("Author:")[0]
            get_name = (
                str(soup.find("aside", {"class": "breadcrumbs"}))
                .rsplit("»", maxsplit=1)[-1]
                .split("</")[0]
                .strip()
                .replace(" ", "-")
            )
            get_difficulty = filter_problem.split("Date Added:")[0].split(
                "Difficulty Rating:"
            )[1]
            problem_name = sub("[^A-Za-z0-9-]+", "", get_name)
            problem_name = problem[0] + f"-{problem_name}"
            difficulty = sub("[^-0-9]+", "", get_difficulty)
            if difficulty:
                for category, score in self.difficulty.items():
                    if int(difficulty) <= score:
                        difficulty = category
                        break
            else:
                difficulty = "NA"
            problem[1] = difficulty
        except Exception as error:
            return "Error!", error, problem
        return problem_name, problem_description, problem
