import logging
import sys
from pathlib import Path

import rich.traceback
from loguru import logger

import qtk.typing as tp
from qtk.logging._handler import InterceptHandler

DEFAULT_FILTER: dict[str | None, str | int | bool] = {
    "everett": logging.INFO,
    "git.cmd": logging.INFO,
    "jax._src": logging.INFO,
    "numba.core": logging.INFO,
    "urllib3.connectionpool": logging.INFO,
}


def init(level: str | int = logging.NOTSET, fpath: tp.StrPath | None = None) -> None:
    rich.traceback.install(show_locals=True)
    logger.remove()
    logger.add(sys.stderr, level=level, filter=DEFAULT_FILTER)
    if fpath is not None:
        fpath: Path = Path(fpath)
        fpath.parent.mkdir(parents=True, exist_ok=True)
        logger.add(fpath.open("w"), level=level, filter=DEFAULT_FILTER)
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
