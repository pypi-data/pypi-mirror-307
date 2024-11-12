from __future__ import annotations

import functools
import time
from typing import TYPE_CHECKING, ParamSpec, TypeVar

from loguru import logger

if TYPE_CHECKING:
    import types
    from collections.abc import Callable

_P = ParamSpec("_P")
_T = TypeVar("_T")


class Timer:
    _end: float
    _start: float
    depth: int | None = None
    level: int | str
    name: str | None

    def __init__(
        self,
        name: str | None = None,
        *,
        depth: int | None = None,
        level: int | str = "DEBUG",
    ) -> None:
        self.name = name
        self.depth = depth
        self.level = level

    def __call__(self, fn: Callable[_P, _T]) -> Callable[_P, _T]:
        if self.name is None:
            self.name = fn.__name__ + "()"
        if self.depth is None:
            self.depth = 3

        @functools.wraps(fn)
        def wrapped(*args: _P.args, **kwargs: _P.kwargs) -> _T:
            with self:
                result: _T = fn(*args, **kwargs)
            return result

        return wrapped

    def __enter__(self) -> None:
        self.start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        self.stop()

    @property
    def elapsed(self) -> float:
        return self._end - self._start

    def start(self) -> None:
        self._start = time.perf_counter()

    def stop(self) -> None:
        self._end = time.perf_counter()
        logger.opt(depth=self.depth or 2).log(
            self.level, "{} executed in {} sec.", self.name or "Block", self.elapsed
        )


timer = Timer
