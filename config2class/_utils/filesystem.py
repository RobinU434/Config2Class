import json
from typing import Any, Callable, Dict

import toml
import yaml


def load_yaml(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "r", encoding=encoding) as file:
        content = yaml.safe_load(file)
    return content


def load_json(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "r", encoding=encoding) as file:
        content = json.load(file)
    return content


def load_toml(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "r", encoding=encoding) as file:
        content = toml.load(file)
    return content


def get_load_func(path: str) -> Callable[[str], Dict[str, Any]]:
    return globals()["load_" + path.split(".")[-1]]


def write_yaml(path: str, content: Dict[str, Any], encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "w", encoding=encoding) as file:
        yaml.dump(content, file)
    return content


def write_json(path: str, content: Dict[str, Any], encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "w", encoding=encoding) as file:
        json.dump(content, file)
    return content


def write_toml(path: str, content: Dict[str, Any], encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "w", encoding=encoding) as file:
        toml.dump(content, file)
    return content


def get_write_func(path: str) -> Callable[[str, Dict[str, Any]], None]:
    return globals()["write_" + path.split(".")[-1]]
