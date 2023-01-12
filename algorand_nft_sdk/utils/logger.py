import logging
import sys


def get_logger() -> logging.Logger:
    file_handler = logging.FileHandler(filename='tmp.log')
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.DEBUG, 
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=handlers
    )

    log = logging.getLogger(__name__)

    return log
