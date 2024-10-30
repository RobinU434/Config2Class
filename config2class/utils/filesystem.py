import json
from typing import Any, Dict

import toml
import yaml


def load_yaml(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, encoding=encoding) as file:
        content = yaml.safe_load(file)
    return content


def load_json(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, encoding=encoding) as file:
        content = json.load(file)
    return content


def load_toml(path: str, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, encoding=encoding) as file:
        content = toml.load(file)
    return content
