# Copyright (C) 2022 Pavocracy <pavocracy@pm.me>
# This file is released as part of leetscraper under GPL-2.0 License.
# Find this project at https://github.com/Pavocracy/leetscraper

"""This module contains the functions to ensure all logging is done to the same file."""

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


def log_message(log_level: str, message: str, *args: object):
    """Send a message to the leetscraper logger. You must specify a log level, a message and pass
    any objects required for the message formatting.
    """
    logger = get_logger()
    if log_level == "debug":
        logger.debug(message, *args)
    if log_level == "info":
        logger.info(message, *args)
    if log_level == "warning":
        logger.warning(message, *args)
    if log_level == "error":
        logger.error(message, *args)
    if log_level == "exception":
        logger.exception(message, *args)
