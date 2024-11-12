from collections.abc import Iterable, Sequence
from typing import Any, TypeGuard


def is_iterable(
    obj: Any, base_type: tuple[type, ...] = (str, bytes)
) -> TypeGuard[Iterable]:
    return isinstance(obj, Iterable) and not isinstance(obj, base_type)


def is_sequence(
    obj: Any, base_type: tuple[type, ...] = (str, bytes)
) -> TypeGuard[Sequence]:
    return isinstance(obj, Sequence) and not isinstance(obj, base_type)
