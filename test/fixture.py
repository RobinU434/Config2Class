import pytest
from test import OUT_PATH

@pytest.fixture(scope="function")
def cleanup():
    yield
    with open(OUT_PATH, "w", encoding="utf-8") as file:
        file.writelines([])
    