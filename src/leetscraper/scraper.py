# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the functions used to do the actual scraping.
Each function will call the website methods for website specific filtering.
"""

from os import makedirs, path, walk
from time import time
from typing import List, Optional

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm
from urllib3 import PoolManager

from .driver import header_constructor, WebdriverType, webdriver_quit
from .logger import log_message
from .website import WebsiteType


def check_problems(website: WebsiteType, scrape_path: str) -> List[str]:
    """Returns a list of all website problems already scraped in the scrape_path."""
    log_message(
        "debug",
        "Checking %s for existing %s problems",
        scrape_path,
        website.website_name,
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
    log_message(
        "debug",
        "Checking for %s scraped_problems in %s took %s seconds",
        website.website_name,
        scrape_path,
        int(stop - start),
    )
    return scraped_problems


def needed_problems(
    website: WebsiteType,
    scraped_problems: List[str],
    scrape_limit: int,
    browsers: dict,
    leetscraper_version: str,
) -> List[List[Optional[str]]]:
    """Returns a list of scrape_limit website problems missing from the scraped_path."""
    log_message(
        "info", "Getting the list of %s problems to scrape", website.website_name
    )
    if website.need_headers:
        browser, browser_version = list(browsers.items())[0]
        website.headers = header_constructor(
            leetscraper_version, browser, browser_version
        )
    http = PoolManager()
    start = time()
    get_problems = website.get_problems(http, scraped_problems, scrape_limit)
    stop = time()
    log_message(
        "debug",
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
    if not get_problems:
        log_message("warning", "Nothing to scrape! get_problems is empty!")
        return 0
    errors = 0
    start = time()
    for problem in tqdm(get_problems):
        errors += create_problem(website, problem, driver, scrape_path)
    stop = time()
    scraped = scrape_limit - errors if scrape_limit > 0 else len(get_problems) - errors
    log_message(
        "debug",
        "Scraping %s %s problems took %s seconds",
        scraped,
        website.website_name,
        int(stop - start),
    )
    webdriver_quit(driver, website.website_name)
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
        log_message(
            "debug",
            "Failed to scrape %s%s! %s",
            website.base_url,
            problem[0],
            error,
        )
        return 1
