import logging
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar, get_type_hints

import git

import qtk
import qtk.typing as tp

_T = TypeVar("_T")
_C = TypeVar("_C", bound=qtk.BaseConfig)


def main(
    *,
    config: dict[str, Any] | None = None,
    exp_name: str | None = None,
    log_file: tp.StrPath | None = "exp.log",
    log_level: int | str = logging.NOTSET,
    tags: list[str] | None = None,
) -> Callable[[Callable[[_C], _T]], Callable[[_C], _T]]:
    def decorator(fn: Callable[[_C], _T]) -> Callable[[_C], _T]:
        def wrapped(cfg: _C) -> _T:
            qtk.logging.init(level=log_level, fpath=log_file)
            exp: qtk.Experiment = qtk.start(name=exp_name, tags=tags)
            exp.log_parameters(cfg.model_dump())
            exp.log_other("entrypoint", _path_relative_to_git_root())
            result: _T = fn(cfg)
            if log_file:
                exp.log_asset(log_file)
            return result

        if fn.__module__ == "__main__":
            cls: type[_C] = get_type_hints(fn)["cfg"]
            cfg: _C = cls(**(config or {}))
            wrapped(cfg)
        return wrapped

    return decorator


def _path_relative_to_git_root(path: tp.StrPath | None = None) -> Path:
    if path is None:
        path = sys.argv[0]
    path = Path(path).absolute()
    repo: git.Repo = git.Repo(search_parent_directories=True)
    git_root: Path = Path(repo.working_tree_dir)  # pyright: ignore [reportArgumentType]
    try:
        return path.relative_to(git_root)
    except ValueError:
        return path
