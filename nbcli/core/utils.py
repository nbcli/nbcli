"""Define Classes and Functions used throughout nbcli."""
import json
import logging
import os
from pathlib import Path
from pynetbox.core.response import Record
from pynetbox.core.endpoint import DetailEndpoint, RODetailEndpoint
from pynetbox.models.dcim import Cables, Termination


def get_nbcli_dir():

    default = Path.home().joinpath('.nbcli')
    return Path(os.environ.get('NBCLI_DIR', str(default)))


def get_nbcli_logger():

    logging.basicConfig(format="[%(levelname)s](%(name)s): %(message)s")
    logger = logging.getLogger('nbcli')
    env_level = os.environ.get('NBCLI_LOGLEVEL', 'WARNING').upper()
    if hasattr(logging, env_level):
        logger.setLevel(getattr(logging, env_level))
    logger.debug('Log level DEBUG set by enviornment.')
    return logger


def auto_cast(string):
    """Convert True, False, and None strings to their type"""
    assert isinstance(string, str)
    if string.lower() == 'none':
        return None
    if string.lower() == 'true':
        return True
    if string.lower() == 'false':
        return False
    if ('{' in string) or ('[' in string):
        try:
            return json.loads(string)
        except:
            return string
    return string

class Trace(Record):
    """Model to use as custom_return for trace DetailEndpoint."""

    near_end = Termination
    cable = Cables
    far_end = Termination

    def __init__(self, values, api, endpoint):

        data = dict(near_end = values[0],
                    cable = values[1],
                    far_end = values[2])
        
        super().__init__(data, api, endpoint)

    def __str__(self):

        if self.cable:
            return '{}[{}] < #{} > {}[{}]'.format(self.near_end.device.name,
                                             self.near_end.name,
                                             self.cable.id,
                                             self.far_end.device.name,
                                             self.far_end.name)
        else:
            return '{}[{}] <'.format(self.near_end.device.name,
                                             self.near_end.name)


def app_model_loc(obj):
    """Derive pynetbox App and Endpoint names from url/endpoint.url."""
    assert isinstance(obj, Record)
    if obj.url:
        url = obj.url
    else:
        url = obj.endpoint.url
    parts = url.replace(obj.api.base_url, '').strip('/').split('/')
    return '.'.join(parts[:2]).replace('-', '_')


def app_model_by_loc(api, loc):
    """Return Endpoint defined by location"""
    assert isinstance(loc, str)
    loc = loc.lower().replace('-', '_')
    app_ep = loc.split('.')
    assert len(app_ep) == 2
    app = getattr(api, app_ep[0])
    ep = getattr(app, app_ep[1])
    return ep


def is_list_of_records(result):

    assert isinstance(result, list) and (len(result) > 0)

    # check all entries are an instance of Record
    rc = [isinstance(e, Record) for e in result].count(True) == len(result)

    # check all entries are the same type
    tc = len(set(type(e) for e in result)) == 1

    return rc and tc


def add_detail_endpoint(model, name, RO=False, custom_return=None):

    assert model in Record.__subclasses__(), 'model must b subclass of Record'

    @property
    def detail_ep(self):
        return DetailEndpoint(self, name, custom_return=custom_return)

    @property
    def ro_detail_ep(self):
        return RODetailEndpoint(self, name, custom_return=custom_return)

    if RO:
        setattr(model, name, ro_detail_ep)
    else:
        setattr(model, name, detail_ep)
