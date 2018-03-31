import io
import os.path
from unittest import mock

import yaml

from warlok.config import get_hub_config


def test_get_hub_config_success(os_path_exists_mock,
                                builtins_open_mock):
    os_path_exists_mock.return_value = True

    config = {
        'github.com': [{
            'username': 'seporaitis',
            'oauth_token': '0123456789',
        }],
    }

    stream = io.StringIO()
    stream.write(yaml.dump(config))
    stream.seek(0)

    builtins_open_mock.return_value = stream

    expected = {
        'github.com': {
            'username': 'seporaitis',
            'oauth_token': '0123456789',
        },
    }

    assert get_hub_config() == expected

    home_dir = os.path.expanduser('~')
    builtins_open_mock.assert_has_calls([
        mock.call(os.path.join(home_dir, '.config/hub'), 'r'),
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
    yaml_load_mock.side_effect = yaml.YAMLError('Error')

    assert get_hub_config() is None

    home_dir = os.path.expanduser('~')
    builtins_open_mock.assert_has_calls([
        mock.call(os.path.join(home_dir, '.config/hub'), 'r'),
    ])

    yaml_load_mock.assert_called_once()
