from itertools import repeat
from nbcli.core.utils import app_model_by_loc


class NbArgs():

#    _nb = None
#    _logger = None
#    _rm = None

    def __init__(self, *args, **kwargs):

        self._args = list()
        self._kwargs = dict()

        self.proc(*kwargs.items())
        self.proc(*args)

    def __bool__(self):
        return bool(self._args) or bool(self._kwargs)

    def __repr__(self):
        return 'NbArgs(args={}, kwargs={})'.format(self._args, self._kwargs)

    def __iter__(self):
        return self._args.__iter__()

    def __getitem__(self, key):
        return self._kwargs[key]

    def keys(self):
        return self._kwargs.keys()

    def proc(self, *args):

        for arg in args:
            if isinstance(arg, tuple) and (len(arg) == 2):
                self._update(*arg)
            elif isinstance(arg, str):
                self._string(arg)

    def _update(self, key, value):
        if key in self._kwargs:
            if isinstance(self._kwargs[key], list):
                self._kwargs[key].append(value)
            else:
                self._kwargs[key] = [self._kwargs[key], value]
        else:
            self._kwargs[key] = value

    def _string(self, string):

        if ':' in string:
            args = list()
            for resol in reversed(string.split('::')):
                al = list()
                for res in resol.split('~'):
                    nba = NbArgs(self._nb)
                    nba.proc(*args)
                    nba.resolve(*res.split(':'), kwargs=nba._kwargs)
                    al += list(nba.kwargs.items())
                args = al
            for arg in args:
                self._update(*arg)
        elif '=' in string:
            kv = string.split('=')
            if (len(kv) == 2) and (len(kv[0]) > 0) and (len(kv[1]) > 0):
                self._update(kv[0], kv[1]) 
            else:
                self._logger.warning("Could not process '%s'", string)
        else:
            self._args.append(string)

    @staticmethod
    def apply_res(result, res, action='get'):

        assert action in ['get', 'post', 'patch']

        rep_items = getattr(res.reply, action) or ()

        replyl = list()

        for rep in rep_items:
            replyl += [(rep[0], getattr(obj, rep[1])) for obj in result]

        return tuple(replyl)

    @classmethod
    def resolve(cls, resstr, *args, kwargs=None, res=None):

        kwargs = kwargs or {}
        nba = cls()

        res = res or nba._nb.nbcli.rm.get(resstr)
        if not res:
            nba._logger.warning("Could not resolve '%s'", resstr)
            return

        ep = app_model_by_loc(nba._nb, res.model)

        nba.proc(*args, *kwargs.items())
        nba.proc(*zip(repeat(res.lookup), nba))

        result = ep.filter(**nba, brief=1)

        return nba, result
