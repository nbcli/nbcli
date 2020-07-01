from pathlib import Path
import os
import sys
import pynetbox
import urllib3
from .utils import logger

class Config():
    """Namespace to hold config options that will be passed to pynetbox."""

    def __init__(self, conf_dir=None, init=False):
        """Create Config object.

        Args:
            conf_dir (str): Alternate configuration file to use.
            init (bool): Seting True will create a new configuration file.
        """
        self.url = None
        self.token = None
        self.private_key_file = None
        self.private_key = None
        self.ssl_verify = True
        self.threading = False

        if conf_dir:
            confdir = Path(conf_dir)
        else:
            confdir = Path.home().joinpath('.nbcli')

        if init:
            self.init(confdir)
            return

        self.load(confdir)

        assert self.url and self.token

    def init(self, confdir):
        """Create a new empty config file."""
        print('Not Implemented')

    def load(self, confdir):
        """Set attributes from configfile or os environment variables."""

        try:
            user_config = {'__builtins__': None}
            with open(str(confdir.joinpath('user_config.py')), 'r') as fh:
                exec(fh.read(), user_config)
        except Exception as e:
            logger.critical('Error loading user_config!')
            logger.critical("Run: 'nbcli init' or specify a '--conf_dir'")
            raise e

        params = ['url',
                  'token',
                  'private_key_file',
                  'private_key',
                  'ssl_verify',
                  'threading']

        for param in params:
            env_var = 'NBCLI_' + param.upper()
            if param in user_config.keys():
                setattr(self, param, user_config[param])
            if env_var in os.environ.keys():
                setattr(self, param, os.environ[env_var])


    def __setattr__(self, name, value):
        """Override strings to None and bool types."""
        if str(value).lower() in ['', 'none']:
            value = None

        if str(value).lower() == 'true':
            value = True

        if str(value).lower() == 'false':
            value = False

        super().__setattr__(name, value)


def get_session(conf_dir=None, init=False):

    conf = Config(conf_dir=conf_dir, init=init)

    if init:
        return

    if conf.ssl_verify is False:
        urllib3.disable_warnings()

    pynb_kwargs = dict(token=conf.token,
                       private_key_file=conf.private_key_file,
                       private_key=conf.private_key,
                       ssl_verify=conf.ssl_verify,
                       threading=conf.threading)

    for arg in ['private_key_file', 'private_key']:
        if not pynb_kwargs[arg]:
            del pynb_kwargs[arg]

    nb = pynetbox.api(conf.url, **pynb_kwargs)

    return nb
