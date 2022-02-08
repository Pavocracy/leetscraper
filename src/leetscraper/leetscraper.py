"""Leetscraper, a coding challenge webscraper for leetcode, and other websites!

This moddule contains the Leetscraper class that when given a string of a supported website,
will set some attributes that will allow coding challenges to be requested, filtered down
to the problem description, and written to a markdown file.

During class instantiation, kwargs can be accepted to define class behaviour.
Calling class functions in different orders will also change the behaviour of this scraper.
See related docstrings for help.
"""

from time import sleep
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

    website_name: "leetcode.com", "projecteuler.net", "codechef.com" ("leetcode.com" is set if ignored)
    scraped_path: "path/to/save/scraped_problems" (Current working directory is set if ignored)
    scrape_limit: Integer of how many problems to scrape at a time (-1 is set if ignored, which is no limit)
    auto_scrape: "True", "False" (True is set if ignored)

    This means calling this class with no arguments will result in all leetcode problems being scraped automatically and saved to the current working directory.
    """

    def __init__(self, **kwargs) -> None:
        self.supported_website = False
        self.website_name = kwargs.get("website_name", "leetcode.com")
        self.scraped_path = kwargs.get("scraped_path", getcwd())
        self.scrape_limit = kwargs.get("scrape_limit", -1)
        if self.scrape_limit is not type(int):
            self.scrape_limit = int(self.scrape_limit)
        auto_scrape = kwargs.get("auto_scrape", True)
        if self.website_name == "leetcode.com":
            self.supported_website = True
            self.website_options = {
                "difficulty": {1: "EASY", 2: "MEDIUM", 3: "HARD"},
                "api_url": "https://leetcode.com/api/problems/all/",
                "base_url": "https://leetcode.com/problems/",
                "problem_description": {
                    "class": "content__u3I1 question-content__JfgR"
                },
            }
        if self.website_name == "projecteuler.net":
            self.supported_website = True
            self.website_options = {
                "difficulty": {33: "EASY", 66: "MEDIUM", 100: "HARD"},
                "api_url": "https://projecteuler.net/recent",
                "base_url": "https://projecteuler.net/problem=",
                "problem_description": {"id": "content"},
            }
        if self.website_name == "codechef.com":
            self.supported_website = True
            self.website_options = {
                "difficulty": {1: "SCHOOL", 2: "EASY", 3: "MEDIUM", 4: "HARD"},
                "api_url": "https://www.codechef.com/api/list/problems/",
                "base_url": "https://www.codechef.com/problems/",
                "problem_description": {"class": "problem-statement"},
            }
        if not self.supported_website:
            print(f"{self.website_name} is not supported by this scraper!")
        if auto_scrape and self.supported_website:
            http = PoolManager(headers={"Connection": "close"})
            scraped_problems = self.scraped_problems()
            needed_problems = self.needed_problems(http, scraped_problems)
            self.scrape_problems(needed_problems)

    def create_webdriver(self) -> webdriver:  # type: ignore[valid-type]
        """Instantiates the webdriver with pre-defined options."""
        options = Options()
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument("--silent")
        options.add_argument("--disable-gpu")
        service = Service(
            ChromeDriverManager(log_level=0, print_first_line=False).install()
        )
        driver = webdriver.Chrome(service=service, options=options)  # type: ignore[operator, call-arg]
        driver.implicitly_wait(0)
        return driver

    def webdriver_quit(self, driver) -> None:
        """Closes the webdriver."""
        print(f"Closing {self.website_name} driver")
        driver.quit()

    def scraped_problems(self) -> List[str]:
        """Returns a list of all website problems already scraped in the scraped_path."""
        print(
            f"Checking {self.scraped_path} for exsisting {self.website_name} problems"
        )
        scraped_problems = []
        for (dirpath, dirnames, filenames) in walk(
            f"{self.scraped_path}/PROBLEMS/{self.website_name}"
        ):
            for file in filenames:
                if file:
                    if self.website_name == "leetcode.com":
                        scraped_problems.append(file.split(".")[0])
                    elif self.website_name == "projecteuler.net":
                        scraped_problems.append(file.split("-")[0])
                    elif self.website_name == "codechef.com":
                        scraped_problems.append(file.split("-")[0])
        return scraped_problems

    def needed_problems(
        self, http: PoolManager, scraped_problems: list
    ) -> List[List[str]]:
        """Returns a list of website problems missing from the scraped_path."""
        print(f"Getting the list of {self.website_name} problems to scrape")
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
                            self.website_options["difficulty"][  # type: ignore[index]
                                problem["difficulty"]["level"]
                            ],
                        ]
                    )
        elif self.website_name == "projecteuler.net":
            request = http.request("GET", self.website_options["api_url"])
            soup = BeautifulSoup(request.data, "html.parser")
            data = soup.find("td", {"class": "id_column"}).get_text()  # type: ignore[union-attr]
            for i in range(1, int(data) + 1):
                if str(i) not in scraped_problems:
                    get_problems.append([str(i), None])  # type: ignore[list-item]
        elif self.website_name == "codechef.com":
            for value in self.website_options["difficulty"].values():  # type: ignore[attr-defined]
                request = http.request(
                    "GET",
                    self.website_options["api_url"] + value.lower() + "?limit=9999",
                )
                data = loads(request.data.decode("utf-8"))
                for problem in data["data"]:
                    if problem["code"] not in scraped_problems:
                        get_problems.append([problem["code"], value])  # type: ignore[list-item]
        return get_problems  # type: ignore[return-value]

    def scrape_problems(self, needed_problems: List[List[str]]) -> None:
        """Scrapes needed_problems limited by scrape_limit. (All problems if -1)"""
        if self.scrape_limit >= len(needed_problems):
            self.scrape_limit = -1
        if self.scrape_limit == 0:
            print("Exiting due to scrape_limit set to 0!")
            return
        if needed_problems:
            print(
                f"Scraping {self.scrape_limit if self.scrape_limit > -1 else len(needed_problems)} {self.website_name} problems"
            )
            driver = self.create_webdriver()
            for problem in tqdm(needed_problems[: self.scrape_limit]):
                self.create_problem(problem, driver)
            self.webdriver_quit(driver)
        else:
            print(f"No {self.website_name} problems to scrape")
        print(f"Completed scraping {self.website_name} Problems")

    def create_problem(self, problem: List[str], driver: webdriver) -> None:  # type: ignore[valid-type]
        """Gets the html source of a problem, filters down to the problem description, creates a file.\n
        Creates files in scraped_path/website_name/DIFFICULTY/problem.md
        """
        try:
            driver.get(self.website_options["base_url"] + problem[0])  # type: ignore[operator, attr-defined]
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "initial-loading")),
                "Timeout limit reached",
            )
            sleep(1)
            html = driver.page_source  # type: ignore[attr-defined]
            soup = BeautifulSoup(html, "html.parser")
            if self.website_name == "leetcode.com":
                problem_description = (
                    soup.find("div", self.website_options["problem_description"])  # type: ignore[union-attr, arg-type]
                    .get_text()
                    .strip()
                )
                problem_name = problem[0]
            elif self.website_name == "projecteuler.net":
                problem_description = (
                    soup.find("div", self.website_options["problem_description"])  # type: ignore[union-attr, arg-type]
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
                for key, value in self.website_options["difficulty"].items():  # type: ignore[attr-defined]
                    if int(difficulty) <= key:
                        problem[1] = value
                        break
                problem_description = (
                    soup.find("div", {"class": "problem_content"})  # type: ignore[union-attr]
                    .get_text()
                    .strip()
                )
            elif self.website_name == "codechef.com":
                problem_description = (
                    soup.find("div", self.website_options["problem_description"])  # type: ignore[union-attr, arg-type]
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
                file.writelines(self.website_options["base_url"] + problem[0] + "\n\n")  # type: ignore[operator]
                file.writelines(problem_description + "\n")
        except Exception as error:
            print(
                f'\nError occurred while scraping {self.website_options["base_url"]}{problem[0]}: {error}'
            )
