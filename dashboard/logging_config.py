"""Centralized logging configuration for the Personal Finance Dashboard.

Every module that needs a logger calls get_logger(__name__) to obtain
one configured consistently: DEBUG-and-above to a rotating log file,
WARNING-and-above to the console.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "dashboard.log")


def get_logger(name: str) -> logging.Logger:
    """Create or retrieve a configured logger for the given module name.

    Args:
        name: The logger name, conventionally __name__ of the calling
            module.

    Returns:
        A logging.Logger configured with a RotatingFileHandler at
        DEBUG level and a StreamHandler at WARNING level. Calling
        this function again with the same name does not attach
        duplicate handlers.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not logger.handlers:
        os.makedirs(LOG_DIR, exist_ok=True)

        file_formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
        )
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger