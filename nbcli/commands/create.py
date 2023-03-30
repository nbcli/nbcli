"""Sub command to create and/or update objects as defined in YAML file."""

import yaml
from nbcli.core.utils import app_model_by_loc
from nbcli.commands.base import BaseSubCommand
from nbcli.commands.tools import NbArgs


class Upsert:
    """Create and/or Update objects defined in dict."""

    def __init__(self, netbox, logger, model, data, res=None, parent=None):
        """Initialize Upsert object."""
        assert (parent is None) or isinstance(parent, Upsert)

        if isinstance(data, list):
            for d in data:
                Upsert(netbox, logger, model, d, parent=parent)
            return

        self.netbox = netbox
        self.logger = logger
        self.model = model
        self.data = data
        self.parent = parent

        self.res = res or netbox.nbcli.rm.get(self.model.split(":")[0])
        self.ep = app_model_by_loc(self.netbox, self.res.model)
        self.args = None
        self.obj = None
        self.children = list()  # list of tuples (model, data, res)

        assert self.res

        self.obj = None

        self.proc_model()

        self.action()

        self.proc_children()

    def _add_parent_arg(self):
        """If self has a parent object, make sure to apply the correct resolve model."""
        if self.parent:
            res = self.parent.res.get(self.res.model) or self.parent.res
            self.args.apply_res([self.parent.obj], res)

    def proc_model(self):
        """Process model string (key), and resolve is needed."""
        gp = True
        kws = None

        # TODO: fix this ugly workaround for addresses.
        if self.model.endswith("^"):
            gp = False
            self.model = self.model[:-1]

        if ":" in self.model:
            self.args = NbArgs(self.netbox)
            alias, kws = self.model.split(":", 1)
            if gp:
                self._add_parent_arg()

            nba, self.obj = self.args.resolve(alias, kws, kwargs=self.args.kwargs, res=self.res)
            if self.obj:
                assert len(self.obj) == 1
                self.obj = self.obj[0]
                self.args = NbArgs(self.netbox, action="patch")
                if not gp:
                    self._add_parent_arg()
            else:
                self.obj = None
                self.args = NbArgs(self.netbox, action="post")
                self.args.proc(*nba.kwargs.items())
        else:
            self.args = NbArgs(self.netbox, action="post")

        self._add_parent_arg()

    def action(self):
        """Perform the create or update action for defined object."""
        for key, value in self.data.items():
            self.proc_data_items(key, value)

        if self.obj:
            self.logger.info("Updating %s with data: %s", str(self.obj), str(self.args.kwargs))
            self.obj.update(self.args.kwargs)
        else:
            self.logger.info("Creating %s with data: %s", self.res.alias, str(self.args.kwargs))
            self.obj = self.ep.create(**self.args.kwargs)

    def proc_data_items(self, key, value, create=False):
        """Process individual key, value pair to determine what to do with it."""
        rstr = key.split(":")[0]
        res = self.res.get(rstr) or self.netbox.nbcli.rm.get(rstr)

        if res:
            if (":" in key) and (value is None):
                self.children.append((key, {}, res))
            elif isinstance(value, (dict, list)):
                self.children.append((key, value, res))
            else:
                self.args.resolve(key, value, res=res)
        else:
            self.args.update(key, value)

    def proc_children(self):
        """Run Upsert on any child objects found."""
        for child in self.children:
            model, data, res = child

            Upsert(self.netbox, self.logger, model, data, res=res, parent=self)


class CreateSubCommand(BaseSubCommand):
    """Create and/or Update objects defined in YAML file."""

    name = "create"
    parser_kwargs = dict(help="Create/Update objects with YAML file.")
    default_loglevel = 20

    def setup(self):
        """Add file argument to create subcommand."""
        self.parser.add_argument("file", type=str, help="YAML file.")

    def run(self):
        """Run command.

        See documentation and reference examples.
        https://nbcli.codeberg.page/latest/commands/create/
        https://nbcli.codeberg.page/latest/reference/create-examples/

        Usage Examples:

        - Create/Update objects defined in YAML file
          $ nbcli create file.yml
        """
        with open(self.args.file) as fh:
            data_stream = yaml.safe_load_all(fh.read())

        for data in data_stream:
            for key, value in data.items():
                assert self.netbox.nbcli.rm.get(key.split(":")[0])
                Upsert(self.netbox, self.logger, key, value, parent=None)
