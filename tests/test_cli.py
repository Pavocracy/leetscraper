import unittest
from os import path
from subprocess import run

from src.leetscraper.logger import log_message
from src.leetscraper.cli import __version__


class TestLeetscraper(unittest.TestCase):
    def test_cli(self):
        cli_path = path.abspath("src/leetscraper/cli.py")
        log_message("warning", "trying to run %s", cli_path)
        output = run(["python3", cli_path, "-v"],
                     capture_output=True, check=True, shell=True)
        if str(output.stderr):
            log_message("error", "stderr! %s", output.stderr)
        if str(output.stdout):
            log_message("warning", "Checking if leetscraper v%s in %s", __version__, str(output.stdout))
        self.assertTrue(f"leetscraper v{__version__}" in str(output.stdout))


if __name__ == "__main__":
    unittest.main()
