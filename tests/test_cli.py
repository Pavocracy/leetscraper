import unittest
from subprocess import run

from src.leetscraper.logger import log_message
from src.leetscraper.cli import __version__


class TestLeetscraper(unittest.TestCase):
    def test_cli(self):
        output = run(["python3", "src/leetscraper/cli.py", "-v"],
                     capture_output=True, check=True, shell=True)
        log_message("warning", "Checking if leetscraper v%s in %s", __version__, str(output.stdout))
        self.assertTrue(f"leetscraper v{__version__}" in str(output.stdout))


if __name__ == "__main__":
    unittest.main()
