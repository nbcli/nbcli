from configparser import ConfigParser
from pathlib import Path
import os
import pynetbox
import urllib3

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
            conffile = Path(conf_dir)
        else:
            conffile = Path.home().joinpath('.nbcli.ini')

        if init:
            self.init(conffile)
            return

        self.load(conffile)

        assert self.url and self.token

    def init(self, conffile):
        """Create a new empty config file."""
        print('Not Implemented')

    def load(self, conffile):
        """Set attributes from configfile or os environment variables."""
        params = ['url',
                  'token',
                  'private_key_file',
                  'private_key',
                  'ssl_verify',
                  'threading']

        config = ConfigParser()
        config.read(conffile)
        pynb_conf = config['pynetbox']

        for key in pynb_conf.keys():
            setattr(self, key, pynb_conf.get(key))

        for param in params:
            env_var = 'NBC_' + param.upper()
            self_value = getattr(self, param)
            env_value = os.environ.get(env_var, self_value)
            if self_value != env_value:
                setattr(self, param, env_value)

    def __setattr__(self, name, value):
        """Override configparser strings to Nond and bool types."""
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
