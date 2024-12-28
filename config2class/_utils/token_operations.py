import re
from typing import Any, Dict
from config2class._utils.dict_operations import flatten_dict


def get_token_content(value: str) -> str:
    return value.strip("{}")


def is_token(value, pattern):
    return isinstance(value, str) and re.search(pattern, str(value))


def build_dependency_graph(d: dict, pattern: str = r"\{\{.*?\}\}"):
    d_flatten = flatten_dict(d)
    dependencies = {}
    for key, value in d_flatten.items():
        if not is_token(value, pattern):
            continue
        dependencies[key] = value.strip("{}")
    return dependencies


def token_in(d: Dict[str, Any], pattern: str = r"\{\{.*?\}\}") -> bool:
    for value in d.values():
        if is_token(value, pattern):
            return True
    return False
