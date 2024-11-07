import pytest
from config2class.entrypoint import Config2Code
from test import OUT_PATH
from test.fixture import cleanup
from config2class.utils import deconstruct_config
from config2class.utils import filesystem

@pytest.mark.parametrize(
    "file_name", ["example.json", "example.yaml", "example.toml", "example_flat.json", "example_flat.yaml", "example_flat.toml"]
)
def test_class_construction(cleanup, file_name: str):
    process = Config2Code()
    input_file = "example/" + file_name
    process.to_code(input_file, OUT_PATH)

    # test from file
    import test.tmp as tmp
    try:
        config = getattr(tmp, "App_config").from_file(input_file)
    except AttributeError:
        config = getattr(tmp, "Config").from_file(input_file)

    ending = file_name.split(".")[-1]
    config_file = getattr(filesystem, f"load_{ending}")(input_file)
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