import logging
import sys
import typing as tp
from pathlib import Path


def get_handler(mode: str, log_format: str, path: tp.Optional[Path] = None):
    if path is None:
        handler = logging.StreamHandler(stream=sys.stdout)
    else:
        path.parent.mkdir(exist_ok=True, parents=True)
        path.touch(exist_ok=True)
        handler = logging.FileHandler(path, mode=mode)
    handler.setFormatter(logging.Formatter(log_format))
    return handler


def init_logger(*,
                logger: logging.Logger,
                mode: str = "a",
                log_format: str = "%(message)s",
                path: tp.Optional[Path] = None,
                level: tp.Optional[int] = logging.DEBUG) -> None:
    if level is not None:
        logger.setLevel(level=level)
    handler = get_handler(mode=mode, log_format=log_format, path=path)
    logger.addHandler(handler)
