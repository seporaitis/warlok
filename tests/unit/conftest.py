from unittest import mock

import pytest


@pytest.fixture
def os_path_exists_mock():
    """Mocks os.path.exists()"""
    with mock.patch('os.path.exists') as mock_exists:
        yield mock_exists
