import unittest
import logging
from shutil import rmtree
from os import path
from src.leetscraper import Leetscraper  # type: ignore[import]


class TestLeetscraper(unittest.TestCase):
    def test_codewars(self):
        leetscraper = Leetscraper(
            website_name="codewars.com",
            scraped_path="./unittesting",
            scrape_limit=3,
            auto_scrape=False,
        )

        # Check auto_scrape=False
        self.assertFalse(
            path.isdir(
                f"{leetscraper.scraped_path}/PROBLEMS/{leetscraper.website_name}"
            )
        )
        self.assertTrue(path.isdir(leetscraper.scraped_path))

        # Check supported_browsers
        avaliable_browsers = leetscraper.check_supported_browsers()
        self.assertTrue(avaliable_browsers)

        # Create a list of browsers to test
        browsers = []
        for browser, version in avaliable_browsers.items():
            browsers.append({browser: version})

        # Check needed_problems
        scraped_problems = []
        needed_problems = leetscraper.needed_problems(scraped_problems)
        self.assertGreater(len(needed_problems), 9000)

        # Check create driver with all browsers
        for index, browser in enumerate(browsers):
            driver = leetscraper.create_webdriver(browser)

            # Check scrape_problems with scrape_limit
            leetscraper.scrape_problems(
                needed_problems[index * leetscraper.scrape_limit :], driver
            )

            # Check scraped_problems
            scraped_problems = leetscraper.scraped_problems()
            self.assertEqual(
                len(scraped_problems),
                ((leetscraper.scrape_limit * (index + 1)) - leetscraper.errors),
            )

        # Cleanup problems and logging
        rmtree(leetscraper.scraped_path)
        logging.shutdown()


if __name__ == "__main__":
    unittest.main()
