import unittest
from src.leetscraper import Leetscraper  # type: ignore[import]


class TestLeetscraper(unittest.TestCase):
    def test_unsupported_website(self):
        with self.assertRaises(Exception):
            Leetscraper(website_name="fakewebsite.com")

    def test_string_for_int(self):
        with self.assertRaises(Exception):
            Leetscraper(scrape_limit="five")


if __name__ == "__main__":
    unittest.main()
