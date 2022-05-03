import unittest
from shutil import rmtree
from os import path, walk
from src.leetscraper import Leetscraper  # type: ignore[import]


class TestLeetscraper(unittest.TestCase):
    def test_default(self):
        leetscraper = Leetscraper(scrape_path="./tests/unittesting", scrape_limit=3)

        # Check scraped_problems
        scraped_problems = []
        for (dirpath, dirnames, filenames) in walk(
            f"./{leetscraper.scrape_path}/PROBLEMS/{leetscraper.website.website_name}"
        ):
            for file in filenames:
                if file:
                    scraped_problems.append(file.split(".")[0])
        self.assertEqual(
            len(scraped_problems),
            leetscraper.scraped,
        )

        # Cleanup problems
        rmtree(leetscraper.scrape_path)


if __name__ == "__main__":
    unittest.main()
