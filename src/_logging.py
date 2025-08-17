import logging
import os
import sys
from enum import Enum


class EnvProperty(Enum):
    SHOW_LOGS = 'SHOW_LOGS'

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',)
SHOW_LOGS = os.environ.get(EnvProperty.SHOW_LOGS.value, None)
print_logs: bool = bool(int(SHOW_LOGS)) if SHOW_LOGS else False


def debug(message: str) -> None:
    if print_logs:
        logging.debug(message)


def info(message: str) -> None:
    if print_logs:
        logging.info(message)


def error(message: str) -> None:
    if print_logs:
        logging.error(message)
