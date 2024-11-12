import json
from pathlib import Path
from typing import Any

import qtk.typing as tp


def load_json(fpath: tp.StrPath) -> Any:
    fpath: Path = Path(fpath)
    with fpath.open() as fp:
        return json.load(fp)


def save_json(fpath: tp.StrPath, data: Any) -> None:
    fpath: Path = Path(fpath)
    with fpath.open("w") as fp:
        json.dump(data, fp)
