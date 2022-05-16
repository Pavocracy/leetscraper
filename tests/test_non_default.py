import unittest
from shutil import rmtree

from src.leetscraper.leetscraper import Leetscraper
from src.leetscraper.scraper import check_problems


class TestLeetscraper(unittest.TestCase):
    def test_default(self):
        # Manually call the setup_scraper, and pass a user-defined get_problems list to scrape
        leetscraper = Leetscraper(
            website_name="leetcode.com",
            scrape_path="./tests/unittesting",
            scrape_limit=3,
            auto_scrape=False,
        )
        leetscraper.driver, leetscraper.get_problems = leetscraper.setup_scraper()
        leetscraper.get_problems = [
            ["number-of-longest-increasing-subsequence", 2],
            ["partition-equal-subset-sum", 2],
            ["minimum-possible-integer-after-at-most-k-adjacent-swaps-on-digits", 3],
        ]
        leetscraper.scraped = leetscraper.start_scraping()

        # Check scraped_problems
        scraped_problems = check_problems(leetscraper.website, leetscraper.scrape_path)
        self.assertEqual(len(scraped_problems), leetscraper.scraped)

        # Cleanup problems
        rmtree(leetscraper.scrape_path)


if __name__ == "__main__":
    unittest.main()
