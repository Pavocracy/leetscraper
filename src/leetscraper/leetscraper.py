# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

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

It uses chrome or firefox with Selenium to scrape problems. If chrome or firefox are not
installed on your machine this scraper will raise an Exception and exit without scraping.
During class initialization, kwargs can be accepted to define class behaviour.
Calling class functions in different orders will also change the behaviour of this scraper.
It was written with automation in mind. If you wish to use these modules individually,
See related docstrings for help.
"""

from os import getcwd

from .driver import create_webdriver, webdriver_quit
from .logger import get_logger
from .scraper import check_problems, needed_problems, scrape_problems
from .system import check_path, check_platform, check_supported_browsers
from .website import set_website


class Leetscraper:
    """Leetscraper requires the following kwargs to initialize:

    website_name: name of a supported website to scrape ("leetcode.com" set if ignored)
    scrape_path: "path/to/save/problems" (Current working directory set if ignored)
    scrape_limit: Integer of how many problems to scrape at a time (no limit set if ignored)
    auto_scrape: "True", "False" (True set if ignored)

    This means calling this class with no arguments will result in all leetcode problems
    being scraped automatically and saved to the current working directory.
    """

    def __init__(self, **kwargs):
        """Initialize leetscraper with default values unless kwargs are given."""
        self.website = set_website(kwargs.get("website_name", "leetcode.com"))
        self.scrape_path = check_path(kwargs.get("scrape_path", getcwd()))
        self.scrape_limit = int(kwargs.get("scrape_limit", -1))
        self.auto_scrape = bool(kwargs.get("auto_scrape", True))
        if self.scrape_limit == 0 or self.scrape_limit < -1:
            message = (
                f"scrape_limit error!: Cannot scrape {self.scrape_limit} problems!"
            )
            logger = get_logger()
            logger.exception(message)
            raise Exception(message)
        if not self.auto_scrape:
            return
        self.driver, self.get_problems = self.setup_scraper()
        self.scraped = self.start_scraping()
        webdriver_quit(self.driver, self.website.website_name)

    def setup_scraper(self) -> tuple:
        """Calling this method is required to setup the arguments needed to scrape."""
        user_platform = check_platform()
        browsers = check_supported_browsers(user_platform)
        scraped_problems = check_problems(self.website, self.scrape_path)
        get_problems = needed_problems(
            self.website, scraped_problems, self.scrape_limit
        )
        driver = create_webdriver(browsers, self.website.website_name)
        return driver, get_problems

    def start_scraping(self) -> int:
        """This method scrapes coding problems from the supported website given to the Leetscraper
        class. It returns a value of scraped problems minus any errors caught by exceptions."""
        scraped = scrape_problems(
            self.website,
            self.driver,
            self.get_problems,
            self.scrape_path,
            self.scrape_limit,
        )
        return scraped
