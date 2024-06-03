from logging import (debug, info, warning, error, DEBUG, INFO,  # noqa: F401
                     WARNING, ERROR)
import logging

__all__ = ['DEBUG', 'INFO', 'WARNING', 'ERROR']


def set_level(level) -> None:
    logging.getLogger('root').setLevel(level)
