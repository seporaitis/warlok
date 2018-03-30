from unittest import mock

import pytest


@pytest.fixture
def os_path_exists_mock():
    """Mocks os.path.exists()"""
    with mock.patch('os.path.exists') as mock_exists:
        yield mock_exists


@pytest.fixture
def yaml_load_mock():
    """Mocks yaml.load()"""
    with mock.patch('yaml.load') as mock_load:
        yield mock_load


@pytest.fixture
def builtins_open_mock():
    """Mocks builtins.open()"""
    with mock.patch('builtins.open', mock.mock_open()) as mock_open:
        yield mock_open
