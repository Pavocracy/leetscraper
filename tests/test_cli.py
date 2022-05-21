import unittest
from subprocess import run

from src.leetscraper.cli import __version__


class TestLeetscraper(unittest.TestCase):
    def test_cli(self):
        output = run(["python", "src/leetscraper/cli.py", "-v"],
                     capture_output=True, check=True, shell=True)
        self.assertTrue(f"leetscraper v{__version__}" in str(output.stdout))


if __name__ == "__main__":
    unittest.main()
