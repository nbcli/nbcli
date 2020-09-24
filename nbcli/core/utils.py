"""Define Classes and Functions used throughout nbcli."""
from collections import namedtuple
from pkg_resources import resource_string
import json
import logging
import os
import yaml
from pathlib import Path
from inspect import getmembers, isclass, ismethod
from textwrap import indent
from pynetbox.core.endpoint import Endpoint
from pynetbox.core.response import Record


class NbNS:
    """NameSpace object for nbcli."""
    def __repr__(self):
        """Print Info about Classes and methods in namespace."""
        def pred(obj):
            return isinstance(obj, NbNS) or ismethod(obj)

        ml = getmembers(self, predicate=pred)
        ht = list([self.__doc__ or ''])
        for m in ml:
            s = '{}.{}:\n{}'.format(type(self).__name__,
                                      m[0],
                                      indent(m[1].__doc__ or '', prefix='  '))
            if not m[0].startswith('_'):
                ht.append(indent(s, prefix='  '))
        return '\n\n'.join(ht)


class NbInfo(NbNS):
    """Desplay information for nbcli."""

    def __init__(self, netbox):

        self._nb = netbox
        self._models = {}

    def models(self):
        """Print model location, and alias."""
        print(self._models)

    def views(self):
        """Print model view name."""
        print(self._models)

    def loaded(self):
        """List pre-loaded models"""

        modeldict = dict()

        for key, value in self._models.items():
            if isinstance(value, Endpoint):
                app = value.url.split('/')[-2].title()
                if app in modeldict.keys():
                    modeldict[app].append((key, value))
                else:
                    modeldict[app] = list()
                    modeldict[app].append((key, value))

        for app, modellist in sorted(modeldict.items()):
            print(app + ':')
            for model in sorted(modellist):
                #if display == 'loc':
                #    obj = Record({}, model[1].api, model[1])
                #    print('  ' + app_model_loc(obj))
                #elif display == 'view':
                #    obj = Record({}, model[1].api, model[1])
                #    print('  ' + get_view_name(obj))
                print('  ' + model[0])



class  Reference(NbNS):

    def __init__(self):

        self.Ref = namedtuple('Ref', ['model',
                                      'alias',
                                      'answer',
                                      'lookup',
                                      'hook'])

        #ident = [('dcim.devices', {}),
        #         ('dcim.device_roles', {}),
        #         ('dcim.device_types', {'lookup': 'model'}),
        #         ('dcim.manufacturers', {}),
        #         ('dcim.interfaces', {}),
        #         ('dcim.sites', {}),
        #         ('dcim.racks', {}),
        #         ('ipam.ip_addresses', {'alias': 'address',
        #                                'answer': 'address',
        #                                'lookup': 'address',
        #                                'hook': 'address'}),
        #         ('tenancy.tenants', {})]

        ident = yaml.safe_load(resource_string('nbcli.core', 'resolve_reference.yml').decode())

        refs = list()

        for key, value in ident.items():

            value = value or {}

            alias = key.strip('s').split('.')[-1]

            r = self.Ref(key,
                         value.get('alias') or alias,
                         value.get('answer') or 'id',
                         value.get('lookup') or 'name',
                         value.get('hook') or '{}_id'.format(alias))

            refs.append(r)

        self.refs = tuple(refs)

    def get(self, string):

        for ref in self.refs:
            if ref.alias == string:
                return ref
        return None



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
    ref = api.nbcli.ref.get(loc)
    if ref:
        loc = ref.model
    app_ep = loc.split('.')
    assert len(app_ep) == 2
    app = getattr(api, app_ep[0])
    ep = getattr(app, app_ep[1])
    return ep


def is_list_of_records(result):

    if isinstance(result, list) and (len(result) > 0):

        # check all entries are an instance of Record
        rc = [isinstance(e, Record) for e in result].count(True) == len(result)

        # check all entries are the same type
        tc = len(set(type(e) for e in result)) == 1

        return rc and tc

    else:
        return False
