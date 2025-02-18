from pathlib import Path
from types import NoneType
from typing import Any, Dict, List
from config2class._core.code_abstraction import ConfigAbstraction
from config2class._utils.replacement import replace_tokens


class ConfigConstructor:
    """
    Constructs a Python dataclass from a nested dictionary representing configuration data.

    Attributes:
        configs (List[ConfigAbstraction]): A list of `ConfigAbstraction` instances,
            each representing a part of the configuration structure.
    """

    def __init__(self):
        """
        Initializes a new `ConfigConstructor` instance.
        """
        self.configs: List[ConfigAbstraction] = []

    def construct(self, config: Dict[str, Any]):
        """
        Parses the given configuration dictionary and constructs `ConfigAbstraction` instances
        to represent the configuration structure.

        Args:
            config (Dict[str, Any]): The configuration dictionary.
        """
        config = replace_tokens(config)
        self.configs = []
        if len(config) > 1:
            name = "Config"
            content = config
        else:
            name, content = list(config.items())[0]

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
            file.writelines([])
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
