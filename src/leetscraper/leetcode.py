# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the Leetcode class and its methods.
Initialisation of the class will set attributes required for most of
the class methods. Some Leetscraper attributes will be required.
"""

from json import loads
from os import walk, path, makedirs
from time import time
from typing import List, Union
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm  # type: ignore[import]
from urllib3 import PoolManager
from .logger import get_logger


class Leetcode:
    """This class contains the methods required to scrape problems for leetcode.com."""

    def __init__(self):
        self.website_name = "leetcode.com"
        self.difficulty = {1: "EASY", 2: "MEDIUM", 3: "HARD"}
        self.api_url = "https://leetcode.com/api/problems/all/"
        self.base_url = "https://leetcode.com/problems/"
        self.problem_description = {"class": "content__u3I1 question-content__JfgR"}

    def scraped_problems(self, scrape_path: str) -> List[str]:
        """Returns a list of all website problems already scraped in the scrape_path."""
        logger = get_logger()
        logger.debug(
            "Checking %s for existing %s problems", scrape_path, self.website_name
        )
        start = time()
        scraped_problems = []
        for (dirpath, dirnames, filenames) in walk(
            f"{scrape_path}/PROBLEMS/{self.website_name}"
        ):
            for file in filenames:
                if file:
                    scraped_problems.append(file.split(".")[0])
        stop = time()
        logger = get_logger()
        logger.debug(
            "Checking for %s scraped_problems in %s took %s seconds",
            self.website_name,
            scrape_path,
            int(stop - start),
        )
        return scraped_problems

    def needed_problems(
        self, scraped_problems: List[str], scrape_limit: int
    ) -> List[List[str]]:
        """Returns a list of website problems missing from the scraped_path."""
        logger = get_logger()
        logger.info("Getting the list of %s problems to scrape", self.website_name)
        start = time()
        http = PoolManager()
        try:
            get_problems = []
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
                    break
        except Exception as error:
            logger = get_logger()
            logger.debug(
                "Failed to get problems for %s. Error: %s", self.website_name, error
            )
        stop = time()
        logger = get_logger()
        logger.debug(
            "Getting list of %s needed_problems for %s took %s seconds",
            scrape_limit if scrape_limit > 0 else len(get_problems),
            self.website_name,
            int(stop - start),
        )
        http.clear()
        return get_problems

    def scrape_problems(
        self,
        driver: Union[webdriver.Firefox, webdriver.Chrome],
        needed_problems: List[List[str]],
        scrape_path: str,
        scrape_limit: int,
    ) -> int:
        """Scrapes the list of needed_problems by calling the create_problem method.
        Returns a count of total problems scraped.
        """
        errors = 0
        start = time()
        for problem in tqdm(needed_problems):
            scrape = self.create_problem(problem, driver, scrape_path)
            errors += scrape
        stop = time()
        scraped = (
            scrape_limit - errors if scrape_limit > 0 else len(needed_problems) - errors
        )
        logger = get_logger()
        logger.debug(
            "Scraping %s %s problems took %s seconds",
            scraped,
            self.website_name,
            int(stop - start),
        )
        return scraped

    def create_problem(
        self,
        problem: List[str],
        driver: Union[webdriver.Firefox, webdriver.Chrome],
        scrape_path: str,
    ) -> int:
        """Gets the html source of a problem, filters to problem description, creates a file.\n
        Creates files in scraped_path/website_name/DIFFICULTY/problem.md\n
        Returns 0 for success and 1 for error.
        """
        try:
            driver.get(self.base_url + problem[0])
            WebDriverWait(driver, 3).until(
                EC.invisibility_of_element_located((By.ID, "initial-loading")),
                "Timeout limit reached",
            )
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            problem_description = (
                soup.find("div", self.problem_description).get_text().strip()
            )
            problem_name = problem[0]
            if not path.isdir(
                f"{scrape_path}/PROBLEMS/{self.website_name}/{problem[1]}/"
            ):
                makedirs(f"{scrape_path}/PROBLEMS/{self.website_name}/{problem[1]}/")
            with open(
                f"{scrape_path}/PROBLEMS/{self.website_name}/{problem[1]}/{problem_name}.md",
                "w",
                encoding="utf-8",
            ) as file:
                file.writelines(self.base_url + problem[0] + "\n\n")
                file.writelines(problem_description + "\n")
            return 0
        except Exception as error:
            logger = get_logger()
            logger.debug(
                "Failed to scrape %s%s! %s",
                self.base_url,
                problem[0],
                error,
            )
            return 1
