import logging
from pathlib import Path


LOG_DIRECTORY = Path(__file__).parent.parent / "logs"
LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIRECTORY / "helpdesk.log"


def get_logger():
    logger = logging.getLogger("HelpdeskSystem")

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.propagate = False

        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        )

        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger