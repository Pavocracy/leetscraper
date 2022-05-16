# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the Projecteuler class and its methods. Initialisation of the class will
set attributes required for most of the class methods. Some Leetscraper attributes will be required.
"""

from re import sub
from typing import List, Optional

from bs4 import BeautifulSoup
from urllib3 import PoolManager

from ..logger import log_message


class Projecteuler:
    """This class contains the methods required to scrape problems for projecteuler.net."""

    def __init__(self):
        """These are the attributes specific to URLs and HTML tags for projecteuler.net."""
        self.website_name = "projecteuler.net"
        self.difficulty = {33: "EASY", 66: "MEDIUM", 100: "HARD"}
        self.api_url = "https://projecteuler.net/recent"
        self.base_url = "https://projecteuler.net/problem="
        self.problem_description = {"id": "content"}
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
            request = http.request("GET", self.api_url, headers=headers)
            soup = BeautifulSoup(request.data, "html.parser")
            data = soup.find("td", {"class": "id_column"}).get_text()
            for i in range(1, int(data) + 1):
                if str(i) not in scraped_problems:
                    get_problems.append([str(i), None])
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
            get_name = filter_problem.split("Published")[0].strip().replace(" ", "-")
            problem_name = sub("[^A-Za-z0-9-]+", "", get_name)
            problem_name = problem[0] + f"-{problem_name}"
            problem_description = (
                soup.find("div", {"class": "problem_content"}).get_text().strip()
            )
            difficulty = filter_problem.split("Difficulty rating: ")[1].split("%")[0]
            for key, value in self.difficulty.items():
                if int(difficulty) <= key:
                    problem[1] = value
                    break
        except IndexError:
            problem[1] = "NA"
        except Exception as error:
            return "Error!", error, problem
        return problem_name, problem_description, problem
