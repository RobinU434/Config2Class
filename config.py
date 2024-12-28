from dataclasses import dataclass
from typing import Any, Dict

from omegaconf import DictConfig, OmegaConf

import config2class.utils.filesystem as fs_utils

from abc import ABC

def preprocess_container(content: Dict[str, Any]) -> Dict[str, Any]:
    first_key, first_value = content.popitem()
    if len(content) == 0 and isinstance(first_value, dict):
        return first_value
    else:
        # add the key value pair back into content
        content[first_key] = first_value
        return content


def get_content(file_path: str, resolve: bool = False) -> Dict[str, Any]:
    ending = file_path.split(".")[-1]
    content = getattr(fs_utils, f"load_{ending}")(file_path)
    content = OmegaConf.create(content)
    content = OmegaConf.to_container(content, resolve=resolve)
    return preprocess_container(content)


class StructuredConfig(ABC):
    @classmethod
    def from_file(cls, file: str, resolve: bool = False) -> "App_config":
        content = get_content(file, resolve=resolve)
        return cls(**content)
    
    @classmethod
    def from_dict_config(cls, config: DictConfig, resolve: bool = False):
        container = OmegaConf.to_container(config, resolve=resolve)
        container = preprocess_container(container)
        return cls(**container)
    
    @classmethod
    def from_container(cls, config: Dict[str, Any]) -> "App_config":
        config = preprocess_container(config)
        return cls(**config)

    def to_file(self, file: str, resolve: bool = False):
        ending = file.split(".")[-1]
        write_func = getattr(fs_utils, f"write_{ending}")
        content = OmegaConf.to_container(self, resolve=resolve)
        write_func(file, content)


@dataclass
class _Credentials(StructuredConfig):
    username: str
    password: str

@dataclass
class _Database(StructuredConfig):
    host: str
    port: int
    credentials: _Credentials

    def __post_init__(self):
        self.credentials = _Credentials(**self.credentials)  # pylint: disable=E1134


@dataclass
class _Caching(StructuredConfig):
    enabled: bool
    cache_size: int


@dataclass
class _Features(StructuredConfig):
    authentication: bool
    caching: _Caching

    def __post_init__(self):
        self.caching = _Caching(**self.caching)  # pylint: disable=E1134


@dataclass
class App_config(StructuredConfig):
    name: str
    version: str
    database: _Database
    features: _Features

    def __post_init__(self):
        self.database = _Database(**self.database)  # pylint: disable=E1134
        self.features = _Features(**self.features)  # pylint: disable=E1134
