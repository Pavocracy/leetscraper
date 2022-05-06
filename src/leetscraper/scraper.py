# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the functions used to do the actual scraping.
Each function will call the website methods for website specific filtering.
"""

from os import walk, path, makedirs
from time import time
from typing import List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from urllib3 import PoolManager

from .logger import get_logger
from .driver import WebdriverType
from .website import WebsiteType


def check_problems(website: WebsiteType, scrape_path: str) -> List[str]:
    """Returns a list of all website problems already scraped in the scrape_path."""
    logger = get_logger()
    logger.debug(
        "Checking %s for existing %s problems", scrape_path, website.website_name
    )
    start = time()
    scraped_problems = []
    for (dirpath, dirnames, filenames) in walk(
        f"{scrape_path}/PROBLEMS/{website.website_name}"
    ):
        for file in filenames:
            if file:
                scraped_problems.append(file.split(website.file_split)[0])
    stop = time()
    logger.debug(
        "Checking for %s scraped_problems in %s took %s seconds",
        website.website_name,
        scrape_path,
        int(stop - start),
    )
    return scraped_problems


def needed_problems(
    website: WebsiteType, scraped_problems: List[str], scrape_limit: int
) -> List[List[str]]:
    """Returns a list of scrape_limit website problems missing from the scraped_path."""
    logger = get_logger()
    logger.info("Getting the list of %s problems to scrape", website.website_name)
    start = time()
    http = PoolManager()
    get_problems = website.get_problems(http, scraped_problems, scrape_limit)
    stop = time()
    logger.debug(
        "Getting list of %s needed_problems for %s took %s seconds",
        scrape_limit if scrape_limit > 0 else len(get_problems),
        website.website_name,
        int(stop - start),
    )
    http.clear()
    return get_problems


def scrape_problems(
    website: WebsiteType,
    driver: WebdriverType,
    get_problems: List[List[str]],
    scrape_path: str,
    scrape_limit: int,
) -> int:
    """Scrapes the list of get_problems by calling the create_problem method.
    Returns a count of total problems scraped.
    """
    errors = 0
    start = time()
    for problem in tqdm(get_problems):
        errors += create_problem(website, problem, driver, scrape_path)
    stop = time()
    scraped = scrape_limit - errors if scrape_limit > 0 else len(get_problems) - errors
    logger = get_logger()
    logger.debug(
        "Scraping %s %s problems took %s seconds",
        scraped,
        website.website_name,
        int(stop - start),
    )
    return scraped


def create_problem(
    website: WebsiteType,
    problem: List[str],
    driver: WebdriverType,
    scrape_path: str,
) -> int:
    """Gets the html source of a problem, calls the website function to filter the problem
    description, and creates a markdown file with the filtered results.\n
    This function saves the file in scraped_path/website_name/DIFFICULTY/problem.md\n
    Returns 0 for success and 1 for error.
    """
    try:
        driver.get(website.base_url + problem[0])
        WebDriverWait(driver, 3).until(
            EC.invisibility_of_element_located((By.ID, "initial-loading")),
            "Timeout limit reached",
        )
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        problem_name, problem_description, problem = website.filter_problem(
            soup, problem
        )
        if problem_name == "Error!":
            raise Exception(problem_description)
        if not path.isdir(
            f"{scrape_path}/PROBLEMS/{website.website_name}/{problem[1]}/"
        ):
            makedirs(f"{scrape_path}/PROBLEMS/{website.website_name}/{problem[1]}/")
        with open(
            f"{scrape_path}/PROBLEMS/{website.website_name}/{problem[1]}/{problem_name}.md",
            "w",
            encoding="utf-8",
        ) as file:
            file.writelines(website.base_url + problem[0] + "\n\n")
            file.writelines(problem_description + "\n")
        return 0
    except Exception as error:
        logger = get_logger()
        logger.debug(
            "Failed to scrape %s%s! %s",
            website.base_url,
            problem[0],
            error,
        )
        return 1
