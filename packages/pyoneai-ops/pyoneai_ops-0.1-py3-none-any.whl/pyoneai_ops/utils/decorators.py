__all__ = [
    "handle_missing_config",
]

import re
from functools import wraps
from typing import Callable


def handle_missing_config(func: Callable):
    _MSG_PATTERN = re.compile(
        r"(.*) No such file or directory: '/etc/one/aiops/(.*)'"
    )

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as err:
            if match := re.match(_MSG_PATTERN, str(err)):
                conf_file = match.group(2)
                raise FileNotFoundError(
                    "Configuration file not found. Please create the "
                    f"configuration file at /etc/one/oneaiops/{conf_file}"
                ) from err
            else:
                raise err

    return wrapper
