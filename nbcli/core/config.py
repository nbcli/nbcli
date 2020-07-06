from pathlib import Path
import os
from pkg_resources import resource_string
import sys
import pynetbox
import requests
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

#        self.conf = type('conf', (), {})()
        self._tree = type('tree', (), {})()

        if conf_dir:
            self._tree.confdir = Path(conf_dir)
        else:
            self._tree.confdir = Path.home().joinpath('.nbcli')

        self._tree.conffile = self._tree.confdir.joinpath('user_config.py')

        if init:
            self._init()
            return

        self._load()


    def _init(self):
        """Create a new empty config file."""

        # Create base directory
        confdir = self._tree.confdir
        if confdir.exists() and not confdir.is_dir():
            logger.critical('%s exists, but is not a directory',
                                 str(confdir.absolute()))
            logger.critical("Move, or specify different directory")
            raise FileExistsError(str(confdir.absolute()))
        else:
            confdir.mkdir(exist_ok=True)

        # Create user_config.py file
        conffile = self._tree.conffile
        if conffile.exists():
            logger.info('%s already exists. Skiping.', str(conffile))
        else:
            conffile.touch()
            with open(str(conffile), 'w') as fh:
                fh.write(resource_string('nbcli.core', 'user_config.default').decode())


    def _load(self):
        """Set attributes from configfile or os environment variables."""

        conffile = self._tree.conffile
        try:
            user_config = dict()
            with open(str(conffile), 'r') as fh:
                exec(fh.read(), dict(), user_config)
        except Exception as e:
            logger.critical('Error loading user_config!')
            logger.critical("Run: 'nbcli init' or specify a '--conf_dir'")
            raise e

        for key, value in user_config.items():
            setattr(self, key, value)

            # get envars
            prefix = key.upper() + '_'

            def has_prefix(ek):
                return ek.find(prefix) == 0

            for envkey in filter(has_prefix, os.environ.keys()):
                attr = envkey[len(prefix):].lower()
                getattr(self, key)[attr] = os.environ.get(envkey)


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

    url = conf.pynetbox['url']
    del conf.pynetbox['url']

    nb = pynetbox.api(url, **conf.pynetbox)
    del conf.pynetbox

    if hasattr(conf, 'requests'):
        reqconf = getattr(conf, 'requests')
        session = requests.Session()
        for key, value in reqconf.items():
            setattr(session, key, value)

        nb.http_session = session
        del conf.requests

    if nb.http_session.verify is False:
        urllib3.disable_warnings()

    nb.nbcli_conf = conf

    return nb
