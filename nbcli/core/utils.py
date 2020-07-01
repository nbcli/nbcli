"""Define Classes and Functions used throughout nbcli."""
import logging
import requests
from pynetbox.core.response import Record
from pynetbox.core.endpoint import DetailEndpoint, RODetailEndpoint


logger = logging.getLogger('nbcli')


class Trace(list):
    """Model to use as custom_return for trace DetailEndpoint."""

    def __init__(self, values, api, endpoint):
        """Create Trace object.
        """
        assert isinstance(values, list)
        for i in values:
            if i:
                a, e, i = i['url'].replace(api.base_url, ''). \
                    strip('/').split('/')
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


def get_req(netbox, url):
    """Perform get request"""

    headers = {'Authorization': 'Token ' + netbox.token}
    reply = requests.get(url, headers=headers, verify=netbox.ssl_verify)

    if reply.ok:
        return reply.json()

    return None

def app_model_loc(obj):
    """Derive pynetbox App and Endpoint names from endpoint.url."""
    assert isinstance(obj, Record)
    parts = obj.endpoint.url.replace(obj.api.base_url, ''). \
        strip('/').split('/')
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
