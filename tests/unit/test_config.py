import io
from unittest import mock

import pytest
import yaml

from warlok.config import get_hub_config


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


def test_get_hub_config_success(os_path_exists_mock,
                                builtins_open_mock):
    os_path_exists_mock.return_value = True

    expected = {
        'github.com': {
            'username': 'seporaitis',
            'oauth_token': '0123456789',
        }
    }

    stream = io.StringIO()
    stream.write(yaml.dump(expected))
    stream.seek(0)

    builtins_open_mock.return_value = stream

    assert get_hub_config() == expected

    builtins_open_mock.assert_has_calls([
        mock.call('~/.config/hub', 'r'),
    ])


def test_get_hub_config_no_file(os_path_exists_mock,
                                yaml_load_mock,
                                builtins_open_mock):
    os_path_exists_mock.return_value = False

    assert get_hub_config() is None

    yaml_load_mock.assert_not_called()
    builtins_open_mock.assert_not_called()


def test_get_hub_config_yaml_error(os_path_exists_mock,
                                   yaml_load_mock,
                                   builtins_open_mock):
    os_path_exists_mock.return_value = True
    yaml_load_mock.side_effect = yaml.YAMLError("Error")

    assert get_hub_config() is None

    builtins_open_mock.assert_has_calls([
        mock.call('~/.config/hub', 'r'),
    ])

    yaml_load_mock.assert_called_once()
