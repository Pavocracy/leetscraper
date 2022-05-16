# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the Codewars class and its methods. Initialisation of the class will set
attributes required for most of the class methods. Some Leetscraper attributes will be required.
"""

from typing import List, Optional

from bs4 import BeautifulSoup
from urllib3 import PoolManager

from ..logger import log_message


class Codewars:
    """This class contains the methods required to scrape problems for codewars.com."""

    def __init__(self):
        """These are the attributes specific to URLs and HTML tags for codewars.com."""
        self.website_name = "codewars.com"
        self.difficulty = {
            8: "EASY",
            7: "EASY",
            6: "MEDIUM",
            5: "MEDIUM",
            4: "HARD",
            3: "HARD",
            2: "EXPERT",
            1: "EXPERT",
        }
        self.api_url = "https://www.codewars.com/api/v1/code-challenges/"
        self.base_url = "https://www.codewars.com/kata/"
        self.problem_description = {"id": "description"}
        self.file_split = "."
        self.need_headers = True

    def get_problems(
        self, http: PoolManager, scraped_problems: List[str], scrape_limit: int
    ) -> List[List[Optional[str]]]:
        """Returns problems to scrape defined by checks in this method."""
        # TODO: Find a better way than this! This is REALLY slow!
        try:
            get_problems: list = []
            headers: dict = {}
            headers["User-Agent"] = self.headers
            if scrape_limit == -1 or scrape_limit > 999:
                log_message(
                    "info",
                    "**NOTE** codewars can take up to 5 minutes to find all problems!",
                )
            for i in range(0, 999):
                request = http.request(
                    "GET",
                    self.base_url + f"?page={i}",
                    headers=headers,
                )
                soup = BeautifulSoup(request.data, "html.parser")
                data = soup.find_all("div", {"class": "list-item-kata"})
                if data:
                    for problem in data:
                        if problem["id"] not in scraped_problems:
                            get_problems.append([problem["id"], None])
                            if scrape_limit > 0 and len(get_problems) >= scrape_limit:
                                return get_problems
                else:
                    break
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
            difficulty = self.difficulty[
                (
                    int(
                        soup.find("div", {"class": "inner-small-hex"})
                        .get_text()
                        .split(" ")[0]
                    )
                )
            ]
        except ValueError:
            difficulty = "BETA"
            problem[1] = difficulty
        except Exception as error:
            return "Error!", error, problem
        return problem_name, problem_description, problem
