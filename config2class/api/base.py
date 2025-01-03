from abc import ABC
from typing import Any, Dict

from omegaconf import DictConfig, OmegaConf

from config2class._utils.deconstruction import deconstruct_config
import config2class._utils.filesystem as fs_utils
from config2class.api.construct import get_content, preprocess_container


class StructuredConfig(ABC):
    @classmethod
    def from_file(cls, file: str, resolve: bool = False) -> object:
        content = get_content(file, resolve=resolve)
        return cls(**content)
    
    @classmethod
    def from_dict_config(cls, config: DictConfig, resolve: bool = False) -> object:
        container = OmegaConf.to_container(config, resolve=resolve)
        container = preprocess_container(container)
        return cls(**container)
    
    @classmethod
    def from_container(cls, config: Dict[str, Any]) -> object:
        config = preprocess_container(config)
        return cls(**config)

    def to_file(self, file: str, resolve: bool = False):
        ending = file.split(".")[-1]
        write_func = getattr(fs_utils, f"write_{ending}")
        dict_config = OmegaConf.create(self)
        content = OmegaConf.to_container(dict_config, resolve=resolve)
        write_func(file, content)

    def to_container(self) -> Dict[str, Any]:
        return deconstruct_config(self)