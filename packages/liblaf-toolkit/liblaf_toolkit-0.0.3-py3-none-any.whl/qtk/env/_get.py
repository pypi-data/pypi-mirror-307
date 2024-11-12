import os
from typing import overload


def get_bool(key: str, default: bool = False) -> bool:  # noqa: FBT001, FBT002
    if val := os.getenv(key):
        val = val.lower()
        # ref: <https://github.com/Delgan/loguru/blob/7ef5b676be31471ca9892713bb28fd9a4d39ddd6/loguru/_defaults.py#L12-L19>
        if val in {"1", "ok", "on", "true", "y", "yes"}:
            return True
        if val in {"0", "false", "n", "no", "nok", "off"}:
            return False
        msg: str = f"Invalid environment variable '{key}' (expected a boolean): '{val}'"
        raise ValueError(msg)
    return default


@overload
def get_str(key: str) -> str | None: ...
@overload
def get_str(key: str, default: str) -> str: ...
def get_str(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)
