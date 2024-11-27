    
import os
import importlib
from config2class.utils import filesystem
from config2class.utils.deconstruction import deconstruct_config
from config2class.utils.replacement import replace_tokens
from test import OUT_PATH

def _check_created_config(input_file: str):
    spec = importlib.util.spec_from_file_location("tmp", OUT_PATH)
    generated_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generated_module)
    
    with open(OUT_PATH, "r", encoding="utf-8") as f:
        content = f.readlines()
    print(f"num lines in {OUT_PATH}: {len(content)}")
    try:
        config_cls = getattr(generated_module, "App_config")
        config = config_cls.from_file(input_file)
    except AttributeError:
        config_cls = getattr(generated_module, "Config")
        config = config_cls.from_file(input_file)

    file_name = input_file.split("/")[-1]
    ending = file_name.split(".")[-1]
    config_file = getattr(filesystem, f"load_{ending}")(input_file)
    config_file = replace_tokens(config_file)
    first_key, first_value = config_file.popitem()
    if len(config_file) == 0 and isinstance(first_value, dict):
        config_file = first_value
    else:
        config_file[first_key] = first_value
    assert deconstruct_config(config) == config_file

def _compare_folder_structure(folder_a, folder_b):
    """Compare structure of folders up to subfolder and file names, ignoring extension."""
    for (_, dirs_a, files_a), (_, dirs_b, files_b) in zip(os.walk(folder_a), os.walk(folder_b)):
        if set(dirs_a) != set(dirs_b):
            return False
        files_a = set(map(lambda file: os.path.splitext(file)[0], files_a))
        files_b = set(map(lambda file: os.path.splitext(file)[0], files_b))
        if files_a != files_b:
            return False
    return True
