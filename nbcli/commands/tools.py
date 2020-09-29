from nbcli.core.utils import app_model_by_loc
from nbcli.core.config import get_session


class NbArgs():

    _nb = get_session()
    _logger = _nb.nbcli.logger

    def __init__(self, *args, **kwargs):

        self.args = list()
        self.kwargs = kwargs

        for arg in args:
            if isinstance(arg, tuple) and (len(arg) == 2):
                self.update(*arg)
            elif isinstance(arg, str):
                self.string(arg)

    def update(self, key, value):
        if key in self.kwargs:
            if isinstance(self.kwargs[key], list):
                self.kwargs[key].append(value)
            else:
                self.kwargs[key] = [self.kwargs[key], value]
        else:
            self.kwargs[key] = value

    def string(self, string):

        if ':' in string:
            args = list()
            for resol in reversed(string.split('::')):
                al = list()
                for res in resol.split('~'):
                    al += self.resolve(*res.split(':'), **NbArgs(*args).kwargs)
                args = al
            for arg in args:
                self.update(*arg)
        elif '=' in string:
            kv = string.split('=')
            if (len(kv) == 2) and (len(kv[0]) > 0) and (len(kv[1]) > 0):
                self.update(kv[0], kv[1]) 
            else:
                self._logger.warning("Could not process '%s'", string)
        else:
            self.args.append(string)

    @staticmethod
    def apply_ref(result, ref, create=False):

        if create:
            key = ref.alias
        else:
            key = ref.hook

        return [(key, getattr(obj, ref.answer)) for obj in result]


    def resolve(self, refstr, *args, **kwargs):

        ref = self._nb.nbcli.ref.get(refstr)
        if not ref:
            self._logger.warning("Could not resolve '%s'", refstr)
            return

        ep = app_model_by_loc(self._nb, ref.model)

        nba = NbArgs(*args, *kwargs.items())
        for arg in nba.args:
            nba.update(ref.lookup, arg)

        result = ep.filter(**nba.kwargs)

        return self.apply_ref(result, ref)
