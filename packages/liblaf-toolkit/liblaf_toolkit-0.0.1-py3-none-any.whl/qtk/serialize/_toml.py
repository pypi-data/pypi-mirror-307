from pathlib import Path
from typing import Any

import tomlkit

import qtk.typing as tp


def load_toml(fpath: tp.StrPath) -> tomlkit.TOMLDocument:
    fpath: Path = Path(fpath)
    with fpath.open() as fp:
        return tomlkit.load(fp)


def save_toml(fpath: tp.StrPath, data: Any, *, sort_keys: bool = False) -> None:
    fpath: Path = Path(fpath)
    with fpath.open("w") as fp:
        tomlkit.dump(data, fp, sort_keys=sort_keys)
