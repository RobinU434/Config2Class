import os
import pytest
from test import CONFIG_FILES, OUT_PATH

@pytest.fixture(scope="function")
def cleanup():
    yield
    
    with open(OUT_PATH, "w", encoding="utf-8") as file:
        file.writelines([])
    
    for file in CONFIG_FILES:
        try:
            os.remove(f"test/{file}")
        except FileNotFoundError:
            pass