import unittest
import logging
from shutil import rmtree

from src.leetscraper.leetscraper import Leetscraper
from src.leetscraper.scraper import check_problems


class TestLeetscraper(unittest.TestCase):
    def test_default(self):
        leetscraper = Leetscraper(scrape_path="./tests/unittesting", scrape_limit=3)

        # Check scraped_problems
        scraped_problems = check_problems(leetscraper.website, leetscraper.scrape_path)
        self.assertEqual(len(scraped_problems), leetscraper.scraped)

        # Cleanup problems and logging
        rmtree(leetscraper.scrape_path)
        logging.shutdown()


if __name__ == "__main__":
    unittest.main()
