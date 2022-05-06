import unittest
import logging
from shutil import rmtree
from os import path
from src.leetscraper.leetscraper import Leetscraper
from src.leetscraper.driver import create_webdriver, webdriver_quit
from src.leetscraper.scraper import check_problems, needed_problems, scrape_problems
from src.leetscraper.system import check_platform, check_supported_browsers


class TestLeetscraper(unittest.TestCase):
    def test_codechef(self):
        leetscraper = Leetscraper(
            website_name="codechef.com",
            scrape_path="./tests/unittesting",
            scrape_limit=3,
            auto_scrape=False,
        )

        # Check auto_scrape=False
        self.assertFalse(
            path.isdir(
                f"{leetscraper.scrape_path}/PROBLEMS/{leetscraper.website.website_name}"
            )
        )
        self.assertTrue(path.isdir(leetscraper.scrape_path))

        # Check platform
        platform = check_platform()
        self.assertTrue(platform)

        # Check supported_browsers
        avaliable_browsers = check_supported_browsers(platform)
        self.assertTrue(avaliable_browsers)

        # Check needed_problems with scrape_limit
        scraped_problems = []
        get_problems = needed_problems(
            leetscraper.website,
            scraped_problems,
            leetscraper.scrape_limit * len(avaliable_browsers),
        )
        self.assertEqual(
            len(get_problems), (leetscraper.scrape_limit * len(avaliable_browsers))
        )

        # Check create_webdriver with all browsers
        total_scraped = 0
        for browser, version in avaliable_browsers.items():
            test_browser = 1
            driver = create_webdriver(
                {browser: version}, leetscraper.website.website_name
            )

            # Check scrape_problems with scrape_limit
            start = 0
            end = leetscraper.scrape_limit * test_browser
            total_scraped += scrape_problems(
                leetscraper.website,
                driver,
                get_problems[start:end],
                leetscraper.scrape_path,
                leetscraper.scrape_limit,
            )

            # Check driver_quit and iterate counts
            test_browser += 1
            start += leetscraper.scrape_limit
            webdriver_quit(driver, leetscraper.website.website_name)

            # Check scraped_problems
            scraped_problems = check_problems(
                leetscraper.website, leetscraper.scrape_path
            )
            self.assertEqual(len(scraped_problems), total_scraped)

        # Cleanup problems and logging
        rmtree(leetscraper.scrape_path)
        logging.shutdown()


if __name__ == "__main__":
    unittest.main()
