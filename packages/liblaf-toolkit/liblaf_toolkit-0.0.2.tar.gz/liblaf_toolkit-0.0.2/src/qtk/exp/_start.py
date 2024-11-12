import datetime
import secrets

import comet_ml as comet
import git

import qtk


def get_name(name: str | None = None) -> str:
    if name:
        return name
    if name := qtk.env.get_str("EXP_NAME"):
        return name
    now: datetime.datetime = datetime.datetime.now()  # noqa: DTZ005
    return now.strftime("%Y-%m-%dT%H%M%S.%f")


def get_key(key: str | None = None) -> str:
    if key:
        return key
    if key := qtk.env.get_str("EXP_KEY"):
        return key
    return secrets.token_hex(16)


def get_url(key: str | None = None) -> str | None:
    if not key:
        return None
    if (workspace := qtk.env.get_str("COMET_WORKSPACE")) and (
        project_name := qtk.env.get_str("COMET_PROJECT_NAME")
    ):
        return f"https://www.comet.com/{workspace}/{project_name}/{key}"
    return None


def auto_commit(exp_name: str | None = None, exp_key: str | None = None) -> None:
    repo: git.Repo = git.Repo(search_parent_directories=True)
    if not repo.is_dirty():
        return
    repo.git.add(all=True)
    message: str = "chore(exp): auto commit\n\n"
    if exp_name:
        message += f"name : {exp_name}\n"
    if url := get_url(exp_key):
        message += f"url  : {url}\n"
    message = message.strip()
    repo.git.commit(message=message)


def start(*, name: str | None = None, tags: list[str] | None = None) -> qtk.Experiment:
    exp_key: str = get_key()
    exp_name: str = get_name(name)
    if qtk.env.get_bool("EXP_AUTO_COMMIT", default=True):
        auto_commit(exp_name, exp_key)
    exp: comet.BaseExperiment = comet.start(
        experiment_key=exp_key,
        experiment_config=comet.ExperimentConfig(name=exp_name, tags=tags),
    )
    return qtk.Experiment(exp)
