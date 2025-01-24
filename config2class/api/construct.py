from pathlib import Path
from typing import Any, Dict
import config2class._utils.filesystem as fs_utils
from omegaconf import OmegaConf


def preprocess_container(content: Dict[str, Any]) -> Dict[str, Any]:
    """remove single layer for config class if existing

    Args:
        content (Dict[str, Any]): config container

    Returns:
        Dict[str, Any]: config containerq
    """
    first_key, first_value = content.popitem()
    if len(content) == 0 and isinstance(first_value, dict):
        return first_value
    else:
        # add the key value pair back into content
        content[first_key] = first_value
        return content


def get_content(file_path: str | Path, resolve: bool = False) -> Dict[str, Any]:
    """build content from file.

    Args:
        file_path (str): path to config file
        resolve (bool, optional): if you would like to have the config resolved. Defaults to False.

    Returns:
        Dict[str, Any]: config container
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    ending = file_path.suffix.lstrip(". ")
    content = getattr(fs_utils, f"load_{ending}")(file_path)
    content = OmegaConf.create(content)
    content = OmegaConf.to_container(content, resolve=resolve)
    return preprocess_container(content)
