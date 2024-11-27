import shutil
from test import CONFIG_DIRS, OUT_PATH_FOLDER
from test.utils import _compare_folder_structure

import pytest

from config2class.entrypoint import Config2Code


@pytest.mark.parametrize(
    "folder_name",
    CONFIG_DIRS,
)
def test_class_construction(folder_name: str):
    process = Config2Code()
    input_folder = "example/" + folder_name
    process.to_code(input_folder, OUT_PATH_FOLDER)

    # structure correctly recreated
    assert _compare_folder_structure(input_folder, OUT_PATH_FOLDER), "Folder structure dissimilar"

    # cleanup
    shutil.rmtree(OUT_PATH_FOLDER)


