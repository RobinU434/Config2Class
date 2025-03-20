    
import importlib
from config2class._utils import filesystem
from config2class._utils.deconstruction import deconstruct_config
from config2class._utils.replacement import replace_tokens
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
        config = config_cls.from_file(input_file, resolve=False)
    except AttributeError:
        config_cls = getattr(generated_module, "Config")
        config = config_cls.from_file(input_file, resolve=False)

    file_name = input_file.split("/")[-1]
    ending = file_name.split(".")[-1]
    config_file = getattr(filesystem, f"load_{ending}")(input_file)
    config_file = replace_tokens(config_file)
    first_key, first_value = config_file.popitem()
    if len(config_file) == 0 and isinstance(first_value, dict):
        config_file = first_value
    else:
        config_file[first_key] = first_value
    print(config.to_container())
    print(config_file)
    assert config.to_container() == config_file, f" {config.to_container()=}\n{config_file=}"
