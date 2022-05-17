# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module will forever be a mark of my failure as a python programmer.
All I wanted to do was have a __version__ variable inside of the leetscraper __init__
that can be imported to other modules for use in functions, while being the singular
location to update the __version__ variable via automated workflows and accessed by setup.cfg.
But I could not figure out how to stop the cyclic import errors. So here we are, admitting
defeat and making a stand alone module that does nothing else but hold the __version__ for
other modules to use. I hope I can one day laugh at this instead of sigh in sadness.
"""

__version__ = "2.1.1"


def check_version() -> str:
    """Return the current leetscraper version. This is only here to avoid cyclic imports."""
    return __version__
