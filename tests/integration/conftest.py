import shutil
import tempfile

import pytest


@pytest.fixture
def temp_dir():
    dir_name = tempfile.mkdtemp(suffix='-pytest').rstrip('/')

    yield dir_name

    shutil.rmtree(dir_name)
