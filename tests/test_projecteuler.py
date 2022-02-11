import unittest
from shutil import rmtree
from os import path, walk
from urllib3 import PoolManager
from src.leetscraper import Leetscraper  # type: ignore[import]


class TestLeetscraper(unittest.TestCase):
    def test_projecteuler(self):
        leetscraper = Leetscraper(
            website_name="projecteuler.net",
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

        # Check chrome_version
        self.assertTrue(leetscraper.chrome_version)

        # Check needed_problems
        scraped_problems = []
        needed_problems = leetscraper.needed_problems(scraped_problems)
        self.assertGreater(len(needed_problems), 0)

        # Check scrape_problems with scrape_limit
        leetscraper.scrape_problems(needed_problems)
        for (dirpath, dirnames, filenames) in walk(
            f"{leetscraper.scraped_path}/PROBLEMS/{leetscraper.website_name}"
        ):
            for file in filenames:
                if file:
                    scraped_problems.append(file)
        self.assertEqual(
            len(scraped_problems), (leetscraper.scrape_limit - leetscraper.errors)
        )
        rmtree(leetscraper.scraped_path)


if __name__ == "__main__":
    unittest.main()
