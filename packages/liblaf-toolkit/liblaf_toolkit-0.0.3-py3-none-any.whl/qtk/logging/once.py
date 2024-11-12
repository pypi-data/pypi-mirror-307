import functools

from loguru import logger


@functools.cache
def log_once(level: int | str, message: str, *args, **kwargs) -> None:
    logger.opt(depth=1).log(level, message, *args, **kwargs)


trace_once = functools.partial(log_once, "TRACE")
debug_once = functools.partial(log_once, "DEBUG")
info_once = functools.partial(log_once, "INFO")
success_once = functools.partial(log_once, "SUCCESS")
warning_once = functools.partial(log_once, "WARNING")
error_once = functools.partial(log_once, "ERROR")
critical_once = functools.partial(log_once, "CRITICAL")
