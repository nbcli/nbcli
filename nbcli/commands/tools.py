from nbcli.core.utils import app_model_by_loc


class NbArgs():

    def __init__(self, netbox, kwargs=None, action='get'):

        assert action in ['get', 'post', 'patch']
        self._nb = netbox
        self._logger = self._nb.nbcli.logger
        self.args = list()
        self.kwargs = kwargs or {}
        self.action = action

    def __bool__(self):
        return bool(self.args) or bool(self.kwargs)

    def __repr__(self):
        return 'NbArgs(args={}, kwargs={})'.format(self.args, self.kwargs)

    def proc(self, *args):

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
                    nba = NbArgs(self._nb)
                    nba.proc(*args)
                    nba.resolve(*res.split(':'), kwargs=nba.kwargs)
                    al += list(nba.kwargs.items())
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

    def apply_res(self, result, res):

        rep_items = getattr(res.reply, self.action)

        replyl = list()

        if not rep_items:
            return replyl

        for rep in rep_items:
            replyl += [(rep[0], getattr(obj, rep[1])) for obj in result]

        self.proc(*tuple(replyl))

    def resolve(self, resstr, *args, kwargs=None, res=None):

        res = res or self._nb.nbcli.rm.get(resstr)
        if not res:
            self._logger.warning("Could not resolve '%s'", resstr)
            return

        ep = app_model_by_loc(self._nb, res.model)

        nba = NbArgs(self._nb, kwargs=kwargs)
        nba.proc(*args)
        for arg in nba.args:
            nba.update(res.lookup, arg)

        result = ep.filter(**nba.kwargs)

        self.apply_res(result, res)

        return nba, result
