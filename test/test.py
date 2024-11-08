import importlib.util
import pytest
from config2class.entrypoint import Config2Code
from config2class.utils.replacement import replace_tokens
from test import OUT_PATH
from test.fixture import cleanup
from config2class.utils import deconstruct_config
from config2class.utils import filesystem
import importlib
import os


@pytest.mark.parametrize(
    "file_name",
    [
        "example.json",
        "example.yaml",
        "example.toml",
        "example_flat.json",
        "example_flat.yaml",
        "example_flat.toml",
        "example_token.yaml",
    ],
)
def test_class_construction(cleanup, file_name: str):
    process = Config2Code()
    input_file = "example/" + file_name
    process.to_code(input_file, OUT_PATH)

    # test from file
    spec = importlib.util.spec_from_file_location("tmp", "test/tmp.py")
    generated_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generated_module)
    try:
        config = getattr(generated_module, "App_config").from_file(input_file)
    except AttributeError:
        config = getattr(generated_module, "Config").from_file(input_file)

    ending = file_name.split(".")[-1]
    config_file = getattr(filesystem, f"load_{ending}")(input_file)
    config_file = replace_tokens(config_file)
    first_key, first_value = config_file.popitem()
    if len(config_file) == 0 and isinstance(first_value, dict):
        config_file = first_value
    else:
        config_file[first_key] = first_value
    assert deconstruct_config(config) == config_file


def test_unknown_file(cleanup):
    try:
        process = Config2Code()
        input_file = "example/example.pkl"
        process.to_code(input_file, OUT_PATH)
        raise AssertionError("Expected to fail because of unknown file")
    except NotImplementedError:
        # test has passed
        assert True


def test_service(cleanup, input_file):
    # create file
    with open(f"test/input_file", "w", encoding="utf-8") as file:
        file.writelines([])

    