"""Define Classes and Functions used throughout nbcli."""

from collections import namedtuple
import json
import logging
import os
from pathlib import Path
from pynetbox.core.endpoint import Endpoint
from pynetbox.core.response import Record


Resolve = namedtuple('Resolve', ['model', 'alias', 'lookup', 'reply'])
Reply = namedtuple('Reply', ['get', 'post', 'patch'])


class ResMgr():
    """Store and retrieve Resolve objects."""

    def __init__(self, *args, **kwargs):
        """Populate ResMgr with Resolve objects based on args/kwargs."""
        self._res = None
        self._resl = []

        if args:
            self._res = Resolve(*args)

        for key, value in kwargs.items():

            value = value or {}

            if isinstance(value, dict):
                self._proc_res_data(key, value)
            elif isinstance(value, list):
                for data in value:
                    self._proc_res_data(key, data)

        self._resl = tuple(self._resl)

    def _proc_res_data(self, key, data):

        model = key
        alias = data.pop('alias', model.strip('s').split('.')[-1])
        lookup = data.pop('lookup', 'name')
        reply = data.pop('reply', {})
        if isinstance(reply, list):
            reply = Reply(tuple([tuple(i) for i in reply]),
                          tuple([tuple(i) for i in reply]),
                          tuple([tuple(i) for i in reply]))
        elif isinstance(reply, dict):
            # tuple-fy
            get = reply.pop('get', (('{}_id'.format(alias), 'id'),))
            post = reply.pop('post', ((alias, 'id'),))
            patch = reply.pop('patch', post)
            reply = Reply(get, post, patch)

        self._resl.append(ResMgr(model, alias, lookup, reply, **data))

    def __repr__(self):
        """."""
        if self._res:
            return str(self._res)
        else:
            rl = list()
            for res in self._resl:
                if res._resl:
                    rl.append('{}*'.format(res.model))
                else:
                    rl.append(res.model)
            return '{}({})'.format('ResMgr', ', '.join(rl))

    def __iter__(self):
        """Iterate through list of child REsolve objects."""
        return self._resl.__iter__()

    def __getattr__(self, key):
        """Return attribute of Resolve object if defined."""
        if (key in Resolve._fields) and self._res:
            return getattr(self._res, key)

        object.__getattribute__(self, key)

    def get(self, string):
        """Return Resolve object if alias or model matches string."""
        for res in self:
            if res.alias == string:
                return res
            if res.model == string:
                return res
        return None


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


def get_nbcli_dir():
    """Return path of nbcli directory."""
    default = Path.home().joinpath('.nbcli')
    return Path(os.environ.get('NBCLI_DIR', str(default)))


def get_nbcli_logger():
    """Return logger object and set level if defined by env var."""
    logging.basicConfig(format="[%(levelname)s](%(name)s): %(message)s")
    logger = logging.getLogger('nbcli')
    env_level = os.environ.get('NBCLI_LOGLEVEL', 'WARNING').upper()
    if hasattr(logging, env_level):
        logger.setLevel(getattr(logging, env_level))
    logger.debug('Log level DEBUG set by enviornment.')
    return logger


def auto_cast(string):
    """Convert True, False, and None strings to their type."""
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
        except Exception:
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
    """Return Endpoint defined by location."""
    assert isinstance(loc, str)
    loc = loc.lower().replace('-', '_')
    res = api.nbcli.rm.get(loc)
    if res:
        loc = res.model
    app_ep = loc.split('.')
    assert len(app_ep) == 2
    app = getattr(api, app_ep[0])
    ep = getattr(app, app_ep[1])
    return ep


def is_list_of_records(result):
    """Determine if list only contains pynetbox Records of the same type."""
    if isinstance(result, list) and (len(result) > 0):

        # check all entries are an instance of Record
        rc = [isinstance(e, Record) for e in result].count(True) == len(result)

        # check all entries are the same type
        tc = len(set(type(e) for e in result)) == 1

        return rc and tc

    else:
        return False


def getter(obj, string):
    """Get attribute or item from object defined by string."""
    assert isinstance(string, str)
    def getitem(o, k):

        try:
            try:
                return o[str(k)]
            except Exception:
                return o[int(k)]
        except Exception:
            return None

    for attr in string.split('.'):
        keys = attr.split(':')[1:]
        attr = attr.split(':')[0]
        try:
            obj = getattr(obj, attr)
            for key in keys:
                obj = getitem(obj, key)
        except Exception:
            return None
    return obj
