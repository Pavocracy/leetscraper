import unittest

from src.leetscraper.leetscraper import Leetscraper


class TestLeetscraper(unittest.TestCase):
    def test_unsupported_website(self):
        with self.assertRaises(Exception):
            Leetscraper(website_name="fakewebsite.com")

    def test_string_for_int(self):
        with self.assertRaises(Exception):
            Leetscraper(scrape_limit="five")

    def test_scrape_limit_zero(self):
        with self.assertRaises(Exception):
            Leetscraper(scrape_limit=0)

    def test_scrape_limit_negitive(self):
        with self.assertRaises(Exception):
            Leetscraper(scrape_limit=-5)


if __name__ == "__main__":
    unittest.main()
