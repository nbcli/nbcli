from configparser import ConfigParser
from pathlib import Path
import os
import urllib3
import pynetbox


class Config():

    def __init__(self, conf_file=None, init=False):

        self.url = None
        self.token = None
        self.private_key_file = None
        self.private_key = None
        self.ssl_verify = True
        self.threading = False

        if conf_file:
            conffile = Path(conf_file)
        else:
            conffile = Path.home().joinpath('.netbox-client.ini')

        if init:
            self.init(conffile)
            return

        self.load(conffile)

        assert self.url and self.token

    def init(self, conffile):
        pass

    def load(self, conffile):

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
            env_var = 'NBCLI_' + param.upper()
            self_value = getattr(self, param)
            env_value = os.environ.get(env_var, self_value)
            if self_value != env_value:
                setattr(self, param, env_value)

    def __setattr__(self, name, value):

        if str(value).lower() in ['', 'none']:
            value = None

        if str(value).lower() == 'true':
            value = True

        if str(value).lower() == 'false':
            value = False

        super().__setattr__(name, value)


def get_session(conf_file=None, init=False):

    conf = Config(conf_file=conf_file, init=init)

    if conf.ssl_verify is False:
        urllib3.disable_warnings()

    pynb_kwargs = dict(token=conf.token,
                     private_key_file=conf.private_key_file,
                     private_key=conf.private_key,
                     ssl_verify=conf.ssl_verify,
                     threading=conf.threading)
    
    for arg in ['private_key_file','private_key']:
        if not pynb_kwargs[arg]:
            del pynb_kwargs[arg]

    nb = pynetbox.api(conf.url, **pynb_kwargs)
    return nb

def add_detail_endpoints():

    @property
    def trace(self):
        return pynetbox.core.endpoint.RODetailEndpoint(self, 'trace')
    
    @property
    def elevation(self):
        return pynetbox.core.endpoint.RODetailEndpoint(self, 'elevation')
    
    pynetbox.models.dcim.Interfaces.trace = trace
    
    pynetbox.models.dcim.Racks.elevation = elevation
