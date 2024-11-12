from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeGuard

import qtk.typing as tp

if TYPE_CHECKING:
    import torch


def is_torch(obj: Any) -> TypeGuard[torch.Tensor]:
    return tp.is_instance_named_partial(obj, "torch.Tensor")
