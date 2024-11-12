import datetime
import shutil
import unittest.mock
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import comet_ml as comet

import qtk
import qtk.typing as tp


def default_name() -> str:
    now: datetime.datetime = datetime.datetime.now()  # noqa: DTZ005
    return now.strftime("%Y-%m-%dT%H%M%S")


class Experiment:
    _exp: comet.BaseExperiment

    def __init__(self, exp: comet.BaseExperiment | None = None) -> None:
        self._exp = exp or comet.get_running_experiment() or unittest.mock.Mock()

    @property
    def project_name(self) -> str:
        return self._exp.project_name or "general"

    @property
    def name(self) -> str:
        return self._exp.get_name()

    def get_parameter(self, name: str) -> Any:
        return self._exp.get_parameter(name)

    def log_parameter(self, name: str, value: Any) -> None:
        self._exp.log_parameter(name, value)

    def log_parameters(self, parameters: dict[str, Any]) -> None:
        self._exp.log_parameters(parameters)

    def log_asset(self, path: tp.StrPath, name: str | None = None) -> None:
        path: Path = Path(path)
        if qtk.env.get_bool("EXP_LOG_ASSET_TO_COMET", default=False):
            self._exp.log_asset(path, name)
        if name is None:
            try:
                name = str(path.absolute().relative_to(Path.cwd()))
            except ValueError:
                name = path.name
        target_path: Path = self.exp_dir / name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target_path)

    @property
    def exp_dir(self) -> Path:
        return self.project_dir / self.name

    @property
    def project_dir(self) -> Path:
        return Path(
            qtk.env.get_str("EXP_PROJECT_DIR")
            or Path.home() / "exp" / self.project_name
        )

    def log_other(self, key: Any, value: Any) -> None:
        self._exp.log_other(key, value)

    def log_others(self, dictionary: Mapping[str, Any]) -> None:
        self._exp.log_others(dictionary)


def get_running_experiment() -> Experiment:
    return Experiment(comet.get_running_experiment())
