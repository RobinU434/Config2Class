import json
from pathlib import Path
from typing import Any, Callable, Dict

import toml
import yaml


def load_yaml(path: str | Path, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "r", encoding=encoding) as file:
        content = yaml.safe_load(file)
    return content


def load_yml(path: str | Path, encoding: str = "utf-8") -> Dict[str, Any]:
    return load_yaml(path, encoding)


def load_json(path: str | Path, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "r", encoding=encoding) as file:
        content = json.load(file)
    return content


def load_jsn(path: str | Path, encoding: str = "utf-8") -> Dict[str, Any]:
    return load_json(path, encoding)


def load_toml(path: str | Path, encoding: str = "utf-8") -> Dict[str, Any]:
    with open(path, "r", encoding=encoding) as file:
        content = toml.load(file)
    return content


def get_load_func(path: str | Path) -> Callable[[str, str], Dict[str, Any]]:
    if isinstance(path, str):
        suffix = path.split(".")[-1]
    elif isinstance(path, Path):
        suffix = path.suffix
    else:
        raise ValueError(f"Not recognized type of `path`: {type(path)}")
    try:
        load_func = globals()["load_" + suffix]
    except KeyError as error:
        raise NotImplementedError(
            f"Files with ending {suffix} are not supported yet. Please use .yaml or .json or .toml."
        ) from error
    return load_func


def get_available_load_funcs() -> Dict[str, Callable[[str, str], Dict[str, Any]]]:
    load_func_names = filter(lambda x: x.split("_")[0] == "load", globals().keys())
    return {k: globals()[k] for k in load_func_names}


def write_yaml(
    path: str | Path, content: Dict[str, Any], encoding: str = "utf-8"
) -> Dict[str, Any]:
    with open(path, "w", encoding=encoding) as file:
        yaml.dump(content, file)
    return content


def write_json(
    path: str | Path, content: Dict[str, Any], encoding: str = "utf-8"
) -> Dict[str, Any]:
    with open(path, "w", encoding=encoding) as file:
        json.dump(content, file)
    return content


def write_toml(
    path: str | Path, content: Dict[str, Any], encoding: str = "utf-8"
) -> Dict[str, Any]:
    with open(path, "w", encoding=encoding) as file:
        toml.dump(content, file)
    return content


def get_write_func(path: str | Path) -> Callable[[str, Dict[str, Any]], None]:
    if isinstance(path, str):
        suffix = path.split(".")[-1]
    elif isinstance(path, Path):
        suffix = path.suffix
    else:
        raise ValueError(f"Not recognized type of `path`: {type(path)}")
    try:
        load_func = globals()["write_" + suffix]
    except KeyError as error:
        raise NotImplementedError(
            f"Files with ending {suffix} are not supported yet. Please use .yaml or .json or .toml."
        ) from error
    return load_func
