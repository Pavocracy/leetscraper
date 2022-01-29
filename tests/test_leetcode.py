import unittest
from src.leetscraper import Leetscraper
from os import path, walk
from urllib3 import PoolManager


class TestLeetscraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.leetscraper = Leetscraper(
            website_name="leetcode.com",
            scraped_path="./leetcode",
            driver_path="./chromedriver",
            scrape_limit=3,
            auto_scrape=False,
        )

    def test_a_auto_scrape_false(self):
        self.assertFalse(
            path.isdir(
                f"{self.leetscraper.scraped_path}/PROBLEMS/{self.leetscraper.website_name}"
            )
        )

    def test_b_scraped_problems_false(self):
        self.assertFalse(self.leetscraper.scraped_problems())

    def test_c_needed_problems(self):
        self.http = PoolManager(headers={"Connection": "close"})
        self.scraped_problems = self.leetscraper.scraped_problems()
        self.needed_problems = self.leetscraper.needed_problems(
            self.http, self.scraped_problems
        )
        self.assertGreater(len(self.needed_problems), 0)

    def test_d_scrape_problems(self):
        self.http = PoolManager(headers={"Connection": "close"})
        self.scraped_problems = self.leetscraper.scraped_problems()
        self.needed_problems = self.leetscraper.needed_problems(
            self.http, self.scraped_problems
        )
        self.leetscraper.scrape_problems(self.needed_problems)
        self.assertTrue(
            path.isdir(
                f"{self.leetscraper.scraped_path}/PROBLEMS/{self.leetscraper.website_name}"
            )
        )

    def test_e_scrape_limit(self):
        scraped_problems = []
        for (dirpath, dirnames, filenames) in walk(
            f"{self.leetscraper.scraped_path}/PROBLEMS/{self.leetscraper.website_name}"
        ):
            for file in filenames:
                if file:
                    scraped_problems.append(file)
        self.assertEqual(len(scraped_problems), self.leetscraper.scrape_limit)


if __name__ == "__main__":
    unittest.main()
