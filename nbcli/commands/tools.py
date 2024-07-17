"""Define Classes and Functions for use by commands."""

from nbcli.core.utils import app_model_by_loc


class NbArgs:
    """Convert list of strings as passed by argparse to a format pynetbox can use."""

    def __init__(self, netbox, kwargs=None, action="get"):
        """Initialize NbArgs object."""
        assert action in ["get", "post", "patch"]
        self._nb = netbox
        self._logger = self._nb.nbcli.logger
        self.args = list()
        self.kwargs = kwargs or {}
        self.action = action

    def __bool__(self):
        """Return False if NbArgs object is 'empty'."""
        return bool(self.args) or bool(self.kwargs)

    def __repr__(self):
        """Meaningful string representation of NbArgs object."""
        return "NbArgs(args={}, kwargs={})".format(self.args, self.kwargs)

    def proc(self, *args):
        """Process raw strings/tuples."""
        for arg in args:
            if isinstance(arg, tuple) and (len(arg) == 2):
                self.update(*arg)
            elif isinstance(arg, str):
                self.string(arg)
            else:
                self._logger.warning(f"Could not process '{arg}'.")

    def update(self, key, value):
        """Add key value to self.kwargs, adding/converting value to list if needed."""
        if key in self.kwargs:
            if isinstance(self.kwargs[key], list):
                self.kwargs[key].append(value)
            else:
                self.kwargs[key] = [self.kwargs[key], value]
        else:
            self.kwargs[key] = value

    def string(self, string):
        """Process raw string, convert to kwarg, or resolve if needed."""

        def proc_kw_string(kw_string):
            """Process string as a keyword argument."""
            kv = string.split("=")
            if (len(kv) == 2) and (len(kv[0]) > 0) and (len(kv[1]) > 0):
                self.update(kv[0], kv[1])
            else:
                self._logger.warning("Could not process '%s'", string)

        def proc_res_string(res_string):
            """Process string as auto-resolve argument."""
            args = list()
            for resol in reversed(string.split("::")):
                al = list()
                for res in resol.split("~"):
                    nba = NbArgs(self._nb, action=self.action)
                    nba.proc(*args)
                    nba.resolve(*res.split(":"), kwargs=nba.kwargs)
                    al += list(nba.kwargs.items())
                args = al
            for arg in args:
                self.update(*arg)

        if "=" in string and ":" in string:
            if string.find("=") < string.find(":"):
                # If the string has both kw token and res token and  kw token comes first
                # Process the string as a kwarg
                proc_kw_string(string)
            else:
                # Process the string as a res_arg
                proc_res_string(string)
        elif ":" in string:
            proc_res_string(string)
        elif "=" in string:
            proc_kw_string(string)
        else:
            self.args.append(string)

    def apply_res(self, result, res):
        """Apply appropriate kwargs for result of resolve."""
        rep_items = getattr(res.reply, self.action)

        replyl = list()

        if not rep_items:
            return replyl

        for rep in rep_items:
            replyl += [(rep[0], getattr(obj, rep[1])) for obj in result]

        self.proc(*tuple(replyl))

    def resolve(self, resstr, *args, kwargs=None, res=None):
        """Try to get results for resstr."""
        res = res or self._nb.nbcli.rm.get(resstr)
        if not res:
            self._logger.warning("Could not resolve '%s'", resstr)
            return

        ep = app_model_by_loc(self._nb, res.model)

        nba = NbArgs(self._nb, kwargs=kwargs)
        nba.proc(*args)
        for arg in nba.args:
            nba.update(res.lookup, arg)

        result = list(ep.filter(**nba.kwargs))

        self.apply_res(result, res)

        return nba, result
