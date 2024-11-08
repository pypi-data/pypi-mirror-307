from importlib import import_module
from typing import Type


def get_class(path: str) -> Type:
    """Get class from path."""
    if "." not in path:
        raise ValueError(f"Invalid path {path}")
    module_name, _, class_name = path.rpartition(".")
    module = import_module(module_name)
    return getattr(module, class_name)
