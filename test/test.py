import importlib
import importlib.util
import os
import shutil
import subprocess
import time
from test import CONFIG_FILES, OUT_PATH
from test.fixture import cleanup
from test.utils import _check_created_config

import pytest

import config2class._service.api_funcs as api_funcs
from config2class._core.entrypoint import Config2Code
from config2class._service.api_funcs import start_service, stop_process
from config2class.utils import deconstruct_config, filesystem
from config2class.utils.replacement import replace_tokens



@pytest.mark.parametrize(
    "file_name",
    CONFIG_FILES,
)
def test_class_construction(cleanup, file_name: str):
    process = Config2Code()
    input_file = "example/" + file_name
    process.file2code(input_file, OUT_PATH)

    # test from file
    _check_created_config(input_file)


def test_unknown_file(cleanup):
    try:
        process = Config2Code()
        input_file = "example/example.pkl"
        process.file2code(input_file, OUT_PATH)
        raise AssertionError("Expected to fail because of unknown file")
    except NotImplementedError:
        # test has passed
        assert True


    

@pytest.mark.parametrize(
    "file_name",
    CONFIG_FILES,
)
def _test_service(cleanup, file_name):
    # create file
    input_file = f"test/{file_name}"
    with open(input_file, "w", encoding="utf-8") as file:
        file.writelines([])

    print(input_file, OUT_PATH)
    pid = start_service(input_file, OUT_PATH, verbose=True)

    with open(input_file, "r", encoding="utf-8") as f:
        content = f.readlines()
    print(f"len of config file {input_file} before copy = {len(content)}")
    
    # copy file content
    # with open("example/" + file_name, "r", encoding="utf-8") as file:
    #     content = file.readlines()
    # with open(input_file, "a", encoding="utf-8") as file:
    #     file.writelines(content)
    
    shutil.copyfile(f"example/{file_name}", input_file)
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.readlines()
    print(f"len of config file {input_file} after copy = {len(content)}")
    
    time.sleep(1)
    stop_process(pid)
    
    _check_created_config(input_file)
    assert False