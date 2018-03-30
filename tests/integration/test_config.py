import os
import tempfile

from warlok.config import get_or_create_config


def test_get_or_create_config(temp_dir):
    config = get_or_create_config(temp_dir)

    assert os.path.exists(os.path.join(temp_dir, "config"))

    assert config is not None


def test_get_or_create_config_create_dir():
    with tempfile.TemporaryDirectory() as dir_name:
        pass

    config = get_or_create_config(dir_name)
    assert config is not None

    assert os.path.exists(os.path.join(dir_name, "config"))
    os.unlink(os.path.join(dir_name, "config"))
    os.rmdir(dir_name)

    assert not os.path.exists(dir_name)


def test_get_or_create_config_callback(temp_dir):
    data = {
        'github.com': {
            'username': 'seporaitis',
            'token': '1234567890'
        }
    }

    config = get_or_create_config(temp_dir, callback=lambda: data)

    assert config['github.com']['username'] == 'seporaitis'
    assert config['github.com']['token'] == '1234567890'


def test_get_or_create_config_does_not_overwrite(temp_dir):
    data1 = {
        'github.com': {
            'username': 'seporaitis',
            'token': '1234567890'
        }
    }

    data2 = {
        'github.com': {
            'username': 'overwritten',
            'token': 'overwritten'
        }
    }

    get_or_create_config(temp_dir, callback=lambda: data1)
    config = get_or_create_config(temp_dir, callback=lambda: data2)

    assert config['github.com']['username'] == 'seporaitis'
    assert config['github.com']['token'] == '1234567890'
