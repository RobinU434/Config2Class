from typing import Any, Dict, List, Union


class ConfigAbstraction:
    """
    This class provides an abstraction for defining configuration data structures. It
    allows creating classes that represent configuration with typed fields and automatic
    generation of dataclasses with post-init logic for nested ConfigAbstraction objects.

    Attributes:
        name (str): The name of the configuration class.
        fields (Dict[str, Any]): A dictionary containing configuration fields and their values.
    """

    def __init__(self, name: str, fields: Dict[str, Any] = None):
        """
        Initializes a new ConfigAbstraction instance.

        Args:
            name (str): The name of the configuration class. This name will be converted
                to PascalCase (e.g., "my_config" becomes "MyConfig"). Leading underscores
                are treated specially, resulting in a single leading underscore in the
                generated class name (e.g., "_private_config" becomes "_PrivateConfig").
            fields (Dict[str, Any], optional): A dictionary containing configuration fields
                and their values. Defaults to None.
        """
        index = 0
        prefix = ""
        if name[0] == "_":
            index = 1
            prefix = "_"
        name = prefix + name[index].upper() + name[index + 1 :]
        self.name = name
        self.fields = fields if fields is not None else {}

    def add_field(
        self, key, value: Union[str, bool, float, list, tuple, int, "ConfigAbstraction"]
    ):
        """
        Adds a new field to the configuration structure.

        Args:
            key (str): The name of the field.
            value (Union[str, bool, float, list, tuple, int, ConfigAbstraction]): The value
                of the field. This can be a primitive type (str, bool, float, int), a
                list, a tuple, or another ConfigAbstraction instance.
        """
        self.fields[key] = value

    def write_code(self) -> List[str]:
        """
        Generates Python code for a dataclass representing the configuration structure.

        Returns:
            List[str]: A list of strings representing the generated Python code.
        """
        code = ["@dataclass\n", f"class {self.name}:\n"]
        post_init = {}
        for key, item in self.fields.items():
            if isinstance(item, ConfigAbstraction):
                typ = item.name
                post_init[key] = item
            else:
                typ = type(item).__name__
            code.append(f"    {key}: {typ}\n")

        # add class method
        code.append("\n    @classmethod")
        code.append(f'\n    def from_file(cls, file: str) -> "{self.name}":')
        code.append("\n        ending = file.split('.')[-1]")
        code.append("\n        content = globals()[f'_load_{ending}'](file)")
        code.append("\n        first_key, first_value = content.popitem()")
        code.append("\n        if len(content) == 0 and isinstance(first_value, dict):")
        code.append("\n            return cls(**first_value)")
        code.append("\n        else:")
        code.append("\n            content[first_key] = first_value")
        code.append("\n        return cls(**content)\n")

        # add post init func
        if len(post_init) == 0:
            return code

        code.append("\n    def __post_init__(self):\n")
        for key, value in post_init.items():
            code.append(
                f"        self.{key} = {value.name}(**self.{key})  #pylint: disable=E1134\n"
            )
        return code
