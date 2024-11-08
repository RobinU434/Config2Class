import importlib
import importlib.util
import os
import shutil
import subprocess
import time
from test import OUT_PATH
from test.fixture import cleanup
from test.utils import _check_created_config

import pytest

import config2class.service.api_funcs as api_funcs
from config2class.entrypoint import Config2Code
from config2class.service.api_funcs import start_observer, stop_process
from config2class.utils import deconstruct_config, filesystem
from config2class.utils.replacement import replace_tokens

CONFIG_FILES = [
    "example.json",
    "example.yaml",
    "example.toml",
    "example_flat.json",
    "example_flat.yaml",
    "example_flat.toml",
    "example_token.yaml",
]


@pytest.mark.parametrize(
    "file_name",
    CONFIG_FILES,
)
def test_class_construction(cleanup, file_name: str):
    process = Config2Code()
    input_file = "example/" + file_name
    process.to_code(input_file, OUT_PATH)

    # test from file
    _check_created_config(input_file)


def test_unknown_file(cleanup):
    try:
        process = Config2Code()
        input_file = "example/example.pkl"
        process.to_code(input_file, OUT_PATH)
        raise AssertionError("Expected to fail because of unknown file")
    except NotImplementedError:
        # test has passed
        assert True


@pytest.mark.parametrize(
    "file_name",
    CONFIG_FILES,
)
def test_service(cleanup, file_name):
    # create file
    input_file = f"test/{file_name}"
    with open(input_file, "w", encoding="utf-8") as file:
        file.writelines([])

    thread = start_observer(input_file, OUT_PATH)
    shutil.copyfile(f"example/{file_name}", input_file)

    stop_process(thread.ident)
    
    _check_created_config(input_file)
    os.remove(input_file)   