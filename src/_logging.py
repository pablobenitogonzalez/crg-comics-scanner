import logging
import os
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',)
logs = os.environ.get('logs', None)
print_logs: bool = bool(int(logs)) if logs else False


def debug(message: str) -> None:
    if print_logs:
        logging.debug(message)


def info(message: str) -> None:
    if print_logs:
        logging.info(message)


def error(message: str) -> None:
    if print_logs:
        logging.error(message)
