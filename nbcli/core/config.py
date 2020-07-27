import os
from pkg_resources import resource_string
import sys
import pynetbox
import requests
import urllib3
import yaml
from nbcli import logger
from nbcli.core.utils import auto_cast, get_nbcli_dir

class Config():
    """Namespace to hold config options that will be passed to pynetbox."""

    def __init__(self, init=False):
        """Create Config object.

        Args:
            init (bool): Seting True will create a new configuration file.
        """

        uf = type('tree', (), {})()

        uf.dir = get_nbcli_dir()
        uf.user_config = uf.dir.joinpath('user_config.yml')
        uf.extdir = uf.dir.joinpath('user_extensions')
        uf.user_commands = uf.extdir.joinpath('user_commands.py')
        uf.user_views = uf.extdir.joinpath('user_views.py')

        self.user_files = uf

        if init:
            self._init()
            return

        self._load()


    def _init(self):
        """Create a new empty config file."""

        # Create user directory tree
        dirlist = [self.user_files.dir, self.user_files.extdir]
        for udir in dirlist:
            if udir.exists() and not udir.is_dir():
                logger.critical('%s exists, but is not a directory',
                                     str(udir.absolute()))
                raise FileExistsError(str(udir.absolute()))
            else:
                udir.mkdir(exist_ok=True)

        # Create user files
        filelist = [self.user_files.user_config,
                    self.user_files.user_commands,
                    self.user_files.user_views]
        for ufile in filelist:
            if ufile.exists():
                logger.info('%s already exists. Skiping.', str(ufile))
            else:
                ufile.touch()
                default = ufile.name + '.default'
                logger.debug(default)
                with open(str(ufile), 'w') as fh:
                    fh.write(resource_string('nbcli.user_defaults',
                                             default).decode())

        print("Edit pynetbox 'url' and 'token' entries in user_config.yml:")
        print('\t{}'.format(str(self.user_files.user_config.absolute())))


    def _load(self):
        """Set attributes from configfile or os environment variables."""

        conffile = self.user_files.user_config
        try:
            user_config = yaml.safe_load(open(str(conffile)))
            #user_config = dict()
            #with open(str(conffile), 'r') as fh:
            #    exec(fh.read(), dict(), user_config)
        except Exception as e:
            logger.critical('Error loading user_config!')
            logger.critical("Run: 'nbcli init' to create a user_config file")
            raise e

        for key, value in user_config.items():
            if isinstance(value, dict):
                setattr(self, key, value)

            # get envars
            prefix = key.upper() + '_'

            def has_prefix(ek):
                return ek.find(prefix) == 0

            for envkey in filter(has_prefix, os.environ.keys()):
                attr = envkey[len(prefix):].lower()
                envval = auto_cast(os.environ.get(envkey))
                getattr(self, key)[attr] = envval


def get_session(init=False):

    conf = Config(init=init)

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
