import logging
import os
import sys

DEBUG_MODE = os.getenv("DEBUG_MODE") in ["True", "true"]


def get_logger() -> logging.Logger:
    file_handler = logging.FileHandler(filename="tmp.log")
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.DEBUG if DEBUG_MODE else logging.INFO,
        format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
        handlers=handlers,
    )

    log = logging.getLogger(__name__)

    return log
