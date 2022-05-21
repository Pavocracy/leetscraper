import unittest
from os import path
from subprocess import run, PIPE

from src.leetscraper.cli import __version__


class TestLeetscraper(unittest.TestCase):
    def test_cli(self):
        cli_path = path.abspath("src/leetscraper/cli.py")
        output = run(["python3", cli_path, "-v"],
                     stdout=PIPE,
                     stderr=PIPE)
        self.assertTrue(f"leetscraper v{__version__}" in str(output.stdout))


if __name__ == "__main__":
    unittest.main()
