from configparser import ConfigParser
from pathlib import Path
import os
import urllib3
import pynetbox
from pynetbox.core.response import Record
from pynetbox.models.dcim import Cables, Interfaces, Termination

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
        print('Not Implemented')

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
            env_var = 'NBC_' + param.upper()
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


class Trace(list):

    def __init__(self, values, api, endpoint):
        assert isinstance(values, list)
        for i in values:
            if i:
                a, e, i = i['url'].replace(api.base_url, '').strip('/').split('/')
                app = getattr(api, a)
                endpoint = getattr(app, e.replace('-', '_'))
                obj = endpoint.get(int(i))
                self.append(obj)
            else:
                self.append(i)

    def __repr__(self):

        if None in self:
            return '{} [{}] <- n/c'.format(self[0].device.name, self[0].name)

        return '{} [{}] <- {} -> {} [{}]'.format(self[0].device.name,
                                             self[0].name, 
                                             str(self[1].id),
                                             self[2].device.name,
                                             self[2].name)


def add_detail_endpoint(model, name, RO=False, custom_return=None):

    assert model in Record.__subclasses__(), 'model must b subclass of Record'

    @property
    def detail_ep(self):
        return pynetbox.core.endpoint.DetailEndpoint(self, name, custom_return=custom_return)

    @property
    def ro_detail_ep(self):
        return pynetbox.core.endpoint.RODetailEndpoint(self, name, custom_return=custom_return)

    if RO:
        setattr(model, name, ro_detail_ep)
    else:
        setattr(model, name, detail_ep)

def is_record(obj):

    obj_class = getattr(obj, '__class__')
    rcd_class = getattr(Record, '__class__')
    return isinstance(obj_class, rcd_class)

def get_session(conf_file=None, init=False):

    conf = Config(conf_file=conf_file, init=init)

    if init:
        return

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

    add_detail_endpoint(pynetbox.models.dcim.Racks,
                        'elevation',
                        RO=True,
                        custom_return=pynetbox.models.dcim.RUs)
    add_detail_endpoint(pynetbox.models.dcim.Interfaces,
                        'trace',
                        RO=True,
                        custom_return=Trace)

    return nb
