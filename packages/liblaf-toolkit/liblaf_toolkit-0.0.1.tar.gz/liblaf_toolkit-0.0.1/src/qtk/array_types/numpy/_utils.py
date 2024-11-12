from __future__ import annotations

from typing import Any, TypeGuard

import numpy as np

import qtk
import qtk.typing as tp


def is_numpy(obj: Any) -> TypeGuard[np.ndarray]:
    return tp.is_instance_named_partial(obj, "numpy.ndarray")


def as_numpy(obj: Any) -> np.ndarray:
    if qtk.is_numpy(obj):
        return obj
    if qtk.is_torch(obj):
        return obj.numpy(force=True)
    return np.asarray(obj)
