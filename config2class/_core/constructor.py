import logging
from pathlib import Path
from types import NoneType
from typing import Any, Dict, List
from config2class._core.code_abstraction import ConfigAbstraction
from config2class.utils.replacement import replace_tokens
from flatten_dict import flatten, unflatten
import pyaml


class ConfigConstructor:
    """
    Constructs a Python dataclass from a nested dictionary representing configuration data.

    Attributes:
        configs (List[ConfigAbstraction]): A list of `ConfigAbstraction` instances,
            each representing a part of the configuration structure.
    """

    def __init__(self, ignore: List[str] = None):
        """
        Initializes a new `ConfigConstructor` instance.
        """
        self.configs: List[ConfigAbstraction] = []
        self.ignore = [] if ignore is None else ignore

    def construct(self, config: Dict[str, Any]):
        """
        Parses the given configuration dictionary and constructs `ConfigAbstraction` instances
        to represent the configuration structure.

        Args:
            config (Dict[str, Any]): The configuration dictionary.
        """
        config = self._filter_ignore(config)

        if len(config.keys()) == 0:
            return
        elif len(config.keys()) == 1:
            name, content = list(config.items())[0]

        elif len(config.keys()) > 1:
            name = "Config"
            content = config

        self.configs = []
        config_abstraction = self._construct_config_class(name, content)
        self.configs.append(config_abstraction)

    def write(self, out_path: str, init_none: bool = False):
        """
        Writes the generated Python code to a file.

        Args:
            out_path (str): The path to the output file.
            init_none (bool, optional): Would you like to init all argument with None or just declare members in the class. Defaults to False

        """
        code = ["from dataclasses import dataclass\n"]
        code.append("from types import NoneType\n")
        code.append("from config2class.api.base import StructuredConfig\n\n\n")

        for abstraction in self.configs:
            code.extend(abstraction.write_code(init_none))
            code.append("\n\n")

        code.pop(-1)
        out_path: Path = Path(out_path)
        if not out_path.exists():
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.touch(exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as file:
            file.writelines([])  # clear file first
            file.writelines(code)

    def _construct_config_class(self, name: str, content: Dict[str, Any]):
        """
        Recursively constructs `ConfigAbstraction` instances for nested configurations.

        Args:
            name (str): The name of the configuration class.
            content (Dict[str, Any]): The configuration dictionary for this level.

        Returns:
            ConfigAbstraction: The constructed `ConfigAbstraction` instance.
        """
        config_abstraction = ConfigAbstraction(name, {})
        for key, value in content.items():
            if isinstance(value, dict) and len(value) > 0:
                sub_config = self._construct_config_class(name="_" + key, content=value)
                self.configs.append(sub_config)
                config_abstraction.add_field(key, sub_config)
            elif isinstance(value, (str, bool, float, list, tuple, int, NoneType)):
                config_abstraction.add_field(key, value)
        return config_abstraction

    def _filter_ignore(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """remove all keys which are specified in self.ignore

        Args:
            config (Dict[str, Any]): config with all keys

        Returns:
            Dict[str, Any]: filtered config
        """
        flattened_config = flatten(config, "dot")
        # check on ignore keys if they are apparent in flattened config
        unaffected_ignores = ""
        filtered_config = {}
        for key in self.ignore:
            if key not in flattened_config.keys():
                unaffected_ignores += f"\t- {key}\n"
            else:
                flattened_config.pop(key)

        if len(unaffected_ignores) > 0:
            yaml_str = pyaml.dump(flattened_config, indent=2)
            yaml_str = " \n\t".join(yaml_str.split("\n"))

            logging.info(
                f"Given the flatted config:\n\t{yaml_str}\n the following keys had no affect:\n{unaffected_ignores}"
            )
        return unflatten(flattened_config, "dot")
