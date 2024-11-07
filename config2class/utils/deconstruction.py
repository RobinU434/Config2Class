from typing import Any, Dict
from dataclasses import is_dataclass


def deconstruct_config(config_obj: object) -> Dict[str, Any]:
    """
    Recursively deconstructs a dataclass object into a dictionary.

    Args:
        config_obj (object): The dataclass object to deconstruct.

    Returns:
        Dict[str, Any]: A dictionary representing the deconstructed dataclass.

    This function iterates over the attributes of the input dataclass. For each attribute:
    1. **If the attribute is a dataclass:** Recursively calls itself to deconstruct the nested dataclass.
    2. **Otherwise:** Directly adds the attribute and its value to the output dictionary.
    """
    config = {}
    for key, value in config_obj.__dict__.items():
        if is_dataclass(value):
            config[key] = deconstruct_config(value)
        else:
            config[key] = value
    return config
