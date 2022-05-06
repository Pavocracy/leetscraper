# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the Projecteuler class and its methods.
Initialisation of the class will set attributes required for most of
the class methods. Some Leetscraper attributes will be required.
"""

from re import sub
from typing import List, Optional

from bs4 import BeautifulSoup
from urllib3 import PoolManager

from src.leetscraper.logger import get_logger


class Projecteuler:
    """This class contains the methods required to scrape problems for projecteuler.net."""

    def __init__(self):
        """These are the attributes specific to URLs and HTML tags for projecteuler.net."""
        # TODO: Handle multiple HTML tags when a website is not consistent?
        self.website_name = "projecteuler.net"
        self.difficulty = {33: "EASY", 66: "MEDIUM", 100: "HARD"}
        self.api_url = "https://projecteuler.net/recent"
        self.base_url = "https://projecteuler.net/problem="
        self.problem_description = {"id": "content"}
        self.file_split = "-"

    def get_problems(
        self, http: PoolManager, scraped_problems: List[str], scrape_limit: int
    ) -> List[List[Optional[str]]]:
        """Returns problems to scrape defined by checks in this method."""
        get_problems = []
        try:
            request = http.request("GET", self.api_url)
            soup = BeautifulSoup(request.data, "html.parser")
            data = soup.find("td", {"class": "id_column"}).get_text()
            for i in range(1, int(data) + 1):
                if str(i) not in scraped_problems:
                    get_problems.append([str(i), None])
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
            get_name = (
                problem_description.split("Published")[0].strip().replace(" ", "-")
            )
            problem_name = sub("[^A-Za-z0-9-]+", "", get_name)
            problem_name = problem[0] + f"-{problem_name}"
            try:
                difficulty = int(
                    problem_description.split("Difficulty rating: ")[1].split("%")[0]
                )
            except IndexError:
                difficulty = 100
            for key, value in self.difficulty.items():
                if int(difficulty) <= key:
                    problem[1] = value
                    break
            problem_description = (
                soup.find("div", {"class": "problem_content"}).get_text().strip()
            )
        except Exception as error:
            return "Error!", error, problem
        return problem_name, problem_description, problem
