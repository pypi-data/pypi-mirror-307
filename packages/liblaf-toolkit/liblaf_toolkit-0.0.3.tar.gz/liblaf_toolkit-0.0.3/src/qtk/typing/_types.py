from os import PathLike
from typing import TypeAlias

from qtk.array_types import ArrayLike

Scalar: TypeAlias = bool | int | float
StrPath: TypeAlias = str | PathLike[str]


__all__ = [
    "ArrayLike",
    "Scalar",
    "StrPath",
]
