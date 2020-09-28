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

    def loaded(self):
        """List pre-loaded models"""

        table = list()
        table.append(['Variable', 'Model Name', 'Alias', 'View Name'])

        for model in self._models.items():
            var = model[0]
            model_name = app_model_loc(model[1])
            alias = '-'
            ref = self._nb.nbcli.ref.get(model_name)
            if ref:
                alias = ref.alias
            view = view_name(model[1])
            table.append([var, model_name, alias, view])

        print(rend_table(table))


def view_name(obj):
    """Generate view name based on class, url, or endpoint url."""
    assert isinstance(obj, (Record, Endpoint))

    class_name = obj.__class__.__name__
    model_loc = app_model_loc(obj)

    if class_name not in ['Record', 'Endpoint']:
        return model_loc.split('.')[0].title() + class_name + 'View'

    return model_loc.title().replace('_', '').replace('.', '') + 'View'


def rend_table(table):
    """Convert 2D array into printable string."""
    assert len(table) > 1
    # get max width for each column
    colw = list()
    for col in range(len(table[0])):
        colw.append(max([len(row[col]) for row in table]))

    # build template based on max with for each column
    template = ''
    buff = 2
    for w in colw:
        template += '{:<' + str(w + buff) + 's}'

    return '\n'.join([template.format(*row) for row in table])


class  Reference(NbNS):

    def __init__(self):

        self.Ref = namedtuple('Ref', ['model',
                                      'alias',
                                      'answer',
                                      'lookup',
                                      'hook'])

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
            if ref.model == string:
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
    assert isinstance(obj, (Record, Endpoint))
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
