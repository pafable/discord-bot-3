# pylint: disable=C0114

import logging
from typing import Final


DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT: Final[str] = "%(asctime)s - %(levelname)s - %(message)s"

def setup_logger(
        date_fmt: str = DATE_FORMAT,
        log_fmt: str = LOG_FORMAT,
        level: int = logging.INFO
    ) -> None:
    """
    Setup logging configuration
    :param date_fmt: 
    :param log_fmt: 
    :param level: 
    :return: 
    """
    logging.basicConfig(
        datefmt=date_fmt,
        format=log_fmt,
        level=level,
    )
