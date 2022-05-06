# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# Signed using RSA key 9A5D2D5AA10873B9ABCD92F1D959AEE8875DEEE6
# This file is released as part of leetscraper under GPL-2.0 License.

"""This module contains the function to ensure all logging is done to the same file."""

import logging
from os import path


def get_logger() -> logging.Logger:
    """Looks for leetscraper logger, otherwise creates a logger.
    All messages to leetscraper.log, INFO and above to console.
    """
    # TODO: Change to logging config file?
    logger = logging.getLogger("leetscraper")
    logger.setLevel(logging.DEBUG)
    formatting = logging.Formatter(
        "%(asctime)s [%(levelname)s]: %(message)s", datefmt="%d %B %Y %I:%M:%S %p"
    )
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(
            f"{path.dirname(__file__)}/leetscraper.log", "a"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatting)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatting)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        print(f"Logging started! Log file: {path.dirname(__file__)}/leetscraper.log")
    return logger
