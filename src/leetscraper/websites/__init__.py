# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""leetscraper currently supports codechef.com, codewars.com, hackerrank.com, leetcode.com, 
projecteuler.net.
"""

__all__ = ["Codechef", "Codewars", "Hackerrank", "Leetcode", "Projecteuler"]

from .codechef import Codechef
from .codewars import Codewars
from .hackerrank import Hackerrank
from .leetcode import Leetcode
from .projecteuler import Projecteuler
