import errno
import os
from configparser import ConfigParser

import yaml


def get_or_create_config(dir_name, file_name='config', callback=None):
    """Get (or create) an instance of ConfigParser.

    Tries to load config file, if directory does not exist -
    creates it and an empty file. If the file was just created -
    populates the file with results of `callback`.`

    Arguments:
    - dir_name  [str]: directory where configuration file(s) are stored.
    - file_name [str]: filename of the file.
    - callback [func]: function that returns dictionary in format:

        {
            'section-name': {
                'config-key': 'config-value',
                'other-key': 'other-value'
            }
        }

    The resulting config file would look like:

        [section-name]
        config-key = config-value
        other-key = other-value

    Returns: ConfigParser

    """

    try:
        os.mkdir(dir_name)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise

    config = ConfigParser()
    file_path = os.path.join(dir_name, file_name)
    if not os.path.exists(file_path):
        open(file_path, 'a').close()

    config.read(file_path)

    if not config.sections() and callback:
        raw = callback()
        if raw:
            for section_name, options in raw.items():
                config.add_section(section_name)
                for option_name, value in options.items():
                    config[section_name][option_name] = value
            with open(file_path, 'w') as file_:
                config.write(file_)

    return config


def get_hub_config():
    """Try to import configuration from `hub` command line tool.

    `hub` is Github native command line tool that Warlok was "piggybacking" on
    in the beginning, so why not just reuse it's credentials - if they're
    found.

    Returns: dictionary in the format specified in `get_or_create_config`.
    """

    path = os.path.join(os.path.expanduser('~'), '.config/hub')
    if not os.path.exists(path):
        return None

    try:
        data = yaml.load(open(path, 'r'))
    except yaml.YAMLError as err:
        return None

    config = {}
    for section_name, options in data.items():
        config[section_name] = {}
        for option_name, value in options[0].items():
            config[section_name][option_name] = value

    return config
