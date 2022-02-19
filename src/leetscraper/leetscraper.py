# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is part of leetscraper which is released under GPL-2.0 License.

"""
  __             __
 |  .-----.-----|  |_.-----.----.----.---.-.-----.-----.----.
 |  |  -__|  -__|   _|__ --|  __|   _|  _  |  _  |  -__|   _|
 |__|_____|_____|____|_____|____|__| |___._|   __|_____|__|
                                           |__|

a coding challenge webscraper for leetcode, and other websites!

This module contains the Leetscraper class that when given the name of a supported
website, will set some attributes that will allow coding challenges to be requested,
filtered down to the problem description, and written to a markdown file.

This scraper currently works for:
leetcode.com, projecteuler.net, codechef.com, hackerrank.com, codewars.com

It uses ChromeDriver with Selenium to scrape problems. If Chrome is not installed
on your machine this scraper will raise an Exception and exit without scraping.
During class instantiation, kwargs can be accepted to define class behaviour.
Calling class functions in different orders will also change the behaviour of this scraper.
It was written with automation in mind. If you wish to use these functions individually,
See related docstrings for help.
"""

import logging
from subprocess import run
from sys import platform
from time import time
from json import loads
from os import getcwd, walk, path, makedirs
from re import sub
from typing import List

from tqdm import tqdm  # type: ignore[import]
from urllib3 import PoolManager
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore[import]


class Leetscraper:
    """Leetscraper requires the following kwargs to instantiate:

    website_name: name of a supported website to scrape ("leetcode.com" set if ignored)
    scraped_path: "path/to/save/scraped_problems" (Current working directory set if ignored)
    scrape_limit: Integer of how many problems to scrape at a time (no limit set if ignored)
    auto_scrape: "True", "False" (True set if ignored)

    This means calling this class with no arguments will result in all leetcode problems
    being scraped automatically and saved to the current working directory.
    """

    def __init__(self, **kwargs):
        supported_website = False
        self.website_name = kwargs.get("website_name", "leetcode.com")
        self.scraped_path = kwargs.get("scraped_path", getcwd())
        self.scrape_limit = kwargs.get("scrape_limit", None)
        auto_scrape = kwargs.get("auto_scrape", True)
        if self.website_name == "leetcode.com":
            supported_website = True
            self.website_options = {
                "difficulty": {1: "EASY", 2: "MEDIUM", 3: "HARD"},
                "api_url": "https://leetcode.com/api/problems/all/",
                "base_url": "https://leetcode.com/problems/",
                "problem_description": {
                    "class": "content__u3I1 question-content__JfgR"
                },
            }
        if self.website_name == "projecteuler.net":
            supported_website = True
            self.website_options = {
                "difficulty": {33: "EASY", 66: "MEDIUM", 100: "HARD"},
                "api_url": "https://projecteuler.net/recent",
                "base_url": "https://projecteuler.net/problem=",
                "problem_description": {"id": "content"},
            }
        if self.website_name == "codechef.com":
            supported_website = True
            self.website_options = {
                "difficulty": {1: "SCHOOL", 2: "EASY", 3: "MEDIUM", 4: "HARD"},
                "api_url": "https://www.codechef.com/api/list/problems/",
                "base_url": "https://www.codechef.com/problems/",
                "problem_description": {"class": "problem-statement"},
            }
        if self.website_name == "hackerrank.com":
            supported_website = True
            self.website_options = {
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
        if self.website_name == "codewars.com":
            supported_website = True
            self.website_options = {
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
        self.logger = self.create_logger()
        if not supported_website:
            message = f"{self.website_name} is not a supported website!"
            self.logger.exception(message)
            raise Exception(message)
        if not path.isdir(self.scraped_path):
            try:
                makedirs(self.scraped_path)
            except Exception as error:
                self.logger.warning(
                    "Could not use path %s! %s. Using %s instead!",
                    self.scraped_path,
                    error,
                    getcwd(),
                )
                self.scraped_path = getcwd()
        if self.scrape_limit == 0:
            message = "Scrape_limit is set to 0!"
            self.logger.exception(message)
            raise Exception(message)
        try:
            if platform.startswith("darwin"):
                check_chrome_version = run(
                    "/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --version",
                    capture_output=True,
                    check=True,
                    shell=True,
                )
            if platform.startswith("linux"):
                check_chrome_version = run(
                    "google-chrome --version",
                    capture_output=True,
                    check=True,
                    shell=True,
                )
            if platform.startswith("win32"):
                check_chrome_version = run(
                    'reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version',
                    capture_output=True,
                    check=True,
                    shell=True,
                )
            get_version = str(check_chrome_version.stdout)
            self.chrome_version = sub("[^0-9.]+", "", get_version)
        except Exception as error:
            message = f"Could not find chrome version! {error}"
            self.logger.exception(message)
            raise Exception(message) from error
        self.errors = 0
        if auto_scrape:
            scraped_problems = self.scraped_problems()
            needed_problems = self.needed_problems(scraped_problems)
            self.scrape_problems(needed_problems)
            logging.shutdown()

    def create_logger(self) -> logging.Logger:
        """Creates the logger. All messages to leetscraper.log, INFO and above to console."""
        logger = logging.getLogger("leetscraper")
        logger.setLevel(logging.DEBUG)
        formatting = logging.Formatter(
            "%(asctime)s [%(levelname)s]: %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p"
        )
        if not logger.hasHandlers():
            file_handler = logging.FileHandler(
                f"{path.dirname(__file__)}/leetscraper.log", "a"
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatting)
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_handler.setFormatter(formatting)
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)
            print(f"Logging start! Log file: {path.dirname(__file__)}/leetscraper.log")
        return logger

    def create_webdriver(self) -> webdriver.chrome.webdriver.WebDriver:
        """Instantiates the webdriver with pre-defined options."""
        options = Options()
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--silent")
        options.add_argument("--disable-gpu")
        if self.website_name == "hackerrank.com":
            options.add_argument(f"user-agent=Chrome/{self.chrome_version}")
        service = Service(
            ChromeDriverManager(log_level=0, print_first_line=False).install()
        )
        driver = webdriver.Chrome(service=service, options=options)  # type: ignore[call-arg]
        driver.implicitly_wait(0)
        self.logger.debug("Created %s webdriver for %s", driver.name, self.website_name)
        return driver

    def webdriver_quit(self, driver):
        """Closes the webdriver."""
        self.logger.debug("Closing %s driver", self.website_name)
        driver.quit()

    def scraped_problems(self) -> List[str]:
        """Returns a list of all website problems already scraped in the scraped_path."""
        self.logger.debug(
            "Checking %s for existing %s problems", self.scraped_path, self.website_name
        )
        start = time()
        scraped_problems = []
        for (dirpath, dirnames, filenames) in walk(
            f"{self.scraped_path}/PROBLEMS/{self.website_name}"
        ):
            for file in filenames:
                if file:
                    if self.website_name == "leetcode.com":
                        scraped_problems.append(file.split(".")[0])
                    if self.website_name == "projecteuler.net":
                        scraped_problems.append(file.split("-")[0])
                    if self.website_name == "codechef.com":
                        scraped_problems.append(file.split("-")[0])
                    if self.website_name == "hackerrank.com":
                        scraped_problems.append(file.split(".")[0])
                    if self.website_name == "codewars.com":
                        scraped_problems.append(file.split(".")[0])
        stop = time()
        self.logger.debug(
            "Checking for %s scraped_problems in %s took %s seconds",
            self.website_name,
            self.scraped_path,
            int(stop - start),
        )
        return scraped_problems

    def needed_problems(self, scraped_problems: list) -> List[List[str]]:
        """Returns a list of website problems missing from the scraped_path."""
        self.logger.info("Getting the list of %s problems to scrape", self.website_name)
        start = time()
        http = PoolManager()
        get_problems = []
        if self.website_name == "leetcode.com":
            request = http.request("GET", self.website_options["api_url"])
            data = loads(request.data.decode("utf-8"))
            for problem in data["stat_status_pairs"]:
                if (
                    problem["stat"]["question__title_slug"] not in scraped_problems
                    and problem["paid_only"] is not True
                ):
                    get_problems.append(
                        [
                            problem["stat"]["question__title_slug"],
                            self.website_options["difficulty"][
                                problem["difficulty"]["level"]
                            ],
                        ]
                    )
        if self.website_name == "projecteuler.net":
            request = http.request("GET", self.website_options["api_url"])
            soup = BeautifulSoup(request.data, "html.parser")
            data = soup.find("td", {"class": "id_column"}).get_text()
            for i in range(1, int(data) + 1):
                if str(i) not in scraped_problems:
                    get_problems.append([str(i), None])
        if self.website_name == "codechef.com":
            for value in self.website_options["difficulty"].values():
                request = http.request(
                    "GET",
                    self.website_options["api_url"] + value.lower() + "?limit=999",
                )
                data = loads(request.data.decode("utf-8"))
                for problem in data["data"]:
                    if problem["code"] not in scraped_problems:
                        get_problems.append([problem["code"], value])
        if self.website_name == "hackerrank.com":
            headers = {}
            chrome_version = f"Chrome/{self.chrome_version}"
            headers["User-Agent"] = chrome_version
            for category in self.website_options["categories"]:
                for i in range(0, 1001, 50):
                    request = http.request(
                        "GET",
                        self.website_options["api_url"]
                        + category
                        + f"/challenges?offset={i}&limit=50",
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
                    else:
                        break
        if self.website_name == "codewars.com":
            self.logger.info(
                "**NOTE** codewars can take up to 5 minutes to find all problems!"
            )
            for i in range(0, 999):
                request = http.request(
                    "GET", self.website_options["base_url"] + f"?page={i}"
                )
                soup = BeautifulSoup(request.data, "html.parser")
                data = soup.find_all("div", {"class": "list-item-kata"})
                if data:
                    for problem in data:
                        if problem["id"] not in scraped_problems:
                            get_problems.append([problem["id"], None])
                else:
                    break
        stop = time()
        self.logger.debug(
            "Getting list of needed_problems for %s took %s seconds",
            self.website_name,
            int(stop - start),
        )
        http.clear()
        return get_problems

    def scrape_problems(self, needed_problems: List[List[str]]):
        """Scrapes needed_problems limited by scrape_limit. (All problems if scrape_limit not set)"""
        if self.scrape_limit:
            if self.scrape_limit >= len(needed_problems):
                self.scrape_limit = None
        if needed_problems:
            self.logger.info(
                "Attempting to scrape %s %s problems",
                self.scrape_limit if self.scrape_limit else len(needed_problems),
                self.website_name,
            )
            start = time()
            driver = self.create_webdriver()
            for problem in tqdm(needed_problems[: self.scrape_limit]):
                self.create_problem(problem, driver)
            self.webdriver_quit(driver)
            stop = time()
            if not self.scrape_limit:
                self.scrape_limit = len(needed_problems)
            self.logger.debug(
                "Scraping %s %s problems took %s seconds",
                self.scrape_limit - self.errors,
                self.website_name,
                int(stop - start),
            )
        else:
            self.logger.warning("No %s problems to scrape", self.website_name)
            return
        if self.errors:
            self.logger.warning(
                "Scraped %s problems, but %s problems failed! Check leetscraper.log for failed scrapes.",
                self.scrape_limit - self.errors
                if self.scrape_limit
                else len(needed_problems) - self.errors,
                self.errors,
            )
        else:
            self.logger.info(
                "Successfully scraped %s %s problems",
                self.scrape_limit if self.scrape_limit else len(needed_problems),
                self.website_name,
            )

    def create_problem(
        self, problem: List[str], driver: webdriver.chrome.webdriver.WebDriver
    ):
        """Gets the html source of a problem, filters down to the problem description, creates a file.\n
        Creates files in scraped_path/website_name/DIFFICULTY/problem.md
        """
        try:
            driver.get(self.website_options["base_url"] + problem[0])
            WebDriverWait(driver, 3).until(
                EC.invisibility_of_element_located((By.ID, "initial-loading")),
                "Timeout limit reached",
            )
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            if self.website_name == "leetcode.com":
                problem_description = (
                    soup.find("div", self.website_options["problem_description"])
                    .get_text()
                    .strip()
                )
                problem_name = problem[0]
            if self.website_name == "projecteuler.net":
                problem_description = (
                    soup.find("div", self.website_options["problem_description"])
                    .get_text()
                    .strip()
                )
                get_name = (
                    problem_description.split("Published")[0].strip().replace(" ", "-")
                )
                problem_name = sub("[^A-Za-z0-9-]+", "", get_name)
                problem_name = problem[0] + f"-{problem_name}"
                try:
                    difficulty = int(
                        problem_description.split("Difficulty rating: ")[1].split("%")[
                            0
                        ]
                    )
                except IndexError:
                    difficulty = 100
                for key, value in self.website_options["difficulty"].items():
                    if int(difficulty) <= key:
                        problem[1] = value
                        break
                problem_description = (
                    soup.find("div", {"class": "problem_content"}).get_text().strip()
                )
            if self.website_name == "codechef.com":
                problem_description = (
                    soup.find("div", self.website_options["problem_description"])
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
            if self.website_name == "hackerrank.com":
                problem_description = (
                    soup.find("div", self.website_options["problem_description"])
                    .get_text()
                    .strip()
                )
                problem_name = problem[0].split("/")[0]
            if self.website_name == "codewars.com":
                try:
                    difficulty = self.website_options["difficulty"][
                        (
                            int(
                                soup.find("div", {"class": "inner-small-hex"})
                                .get_text()
                                .split(" ")[0]
                            )
                        )
                    ]
                except Exception:
                    difficulty = "BETA"  # type: ignore[assignment]
                problem_description = (
                    soup.find("div", self.website_options["problem_description"])
                    .get_text()
                    .strip()
                )
                problem_name = problem[0]
                problem[1] = difficulty  # type: ignore[call-overload]
            if not path.isdir(
                f"{self.scraped_path}/PROBLEMS/{self.website_name}/{problem[1]}/"
            ):
                makedirs(
                    f"{self.scraped_path}/PROBLEMS/{self.website_name}/{problem[1]}/"
                )
            with open(
                f"{self.scraped_path}/PROBLEMS/{self.website_name}/{problem[1]}/{problem_name}.md",
                "w",
                encoding="utf-8",
            ) as file:
                file.writelines(self.website_options["base_url"] + problem[0] + "\n\n")
                file.writelines(problem_description + "\n")
        except Exception as error:
            self.logger.debug(
                "Failed to scrape %s%s %s",
                self.website_options["base_url"],
                problem[0],
                error,
            )
            self.errors += 1
