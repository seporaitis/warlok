import errno
import os
from configparser import ConfigParser


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
                config[section_name] = options
            with open(file_path, 'w') as file_:
                config.write(file_)

    return config
