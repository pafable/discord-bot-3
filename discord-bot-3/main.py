# pylint: disable=C0114,C0116,W0718

import logging
import os
from typing import Final
from dotenv import load_dotenv

from bot import client
from logger import setup_logger


setup_logger()
load_dotenv()

TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")


def main() -> None:
    try:
        client.run(token=TOKEN)
    except Exception as e:
        logging.exception(e)


if __name__ == "__main__":
    main()
