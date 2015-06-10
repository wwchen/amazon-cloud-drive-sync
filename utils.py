from ConfigParser import SafeConfigParser
import os
import sys

REQUIRED_KEYS = [
    'client_id',
    'client_secret',
]

CONFIG_FILES = [
    '~/.amazon-cloud-drive.conf',
    '.amazon-cloud-drive.conf'
]

CONFIG_SECTION = 'Credentials'

def load_file_config(path=None):
    """
    Loads configuration from file with following content::

        [Credentials]
        client_id = <your client id>
        client_secret = <your client secret>

    :param path: path to config file. If not specified, locations
    ``~/.amazon-cloud-drive.conf`` and ``.amazon-cloud-drive.conf`` are tried.
    """
    config = SafeConfigParser()
    if path is None:
        config.read([os.path.expanduser(path) for path in CONFIG_FILES])
    else:
        config.read(path)

    if not config.has_section(CONFIG_SECTION):
        return {}

    return dict(
        (key, val)
        for key, val in config.items(CONFIG_SECTION)
        if key in REQUIRED_KEYS
    )

def load_config(path=None):
    """
    Returns a dict with API credentials which is loaded from (in this order):

    * Config files ``~/.amazon-cloud-drive.conf`` or ``.amazon-cloud-drive.conf``
      where the latter may add or replace values of the former.

    The returned dictionary may look like this::

        {
            'client_id': '<client id>',
            'client_secret': '<client secret>'
        }

    :param path: path to config file.
    """
    config = load_file_config(path)

    # substitute None for all values not found
    for key in REQUIRED_KEYS:
        if key not in config:
            config[key] = None

    return config
