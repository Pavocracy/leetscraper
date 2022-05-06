# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""leetscraper currently supports leetcode.com, projecteuler.net, codechef.com, hackerrank.com,
codewars.com.
"""

__all__ = ["Codechef", "Codewars", "Hackerrank", "Leetcode", "Projecteuler"]

from .codechef import Codechef
from .codewars import Codewars
from .hackerrank import Hackerrank
from .leetcode import Leetcode
from .projecteuler import Projecteuler
