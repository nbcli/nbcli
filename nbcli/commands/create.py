import yaml
from nbcli.commands.base import BaseSubCommand, proc_kw_str


class Upsert():

    def __init__(self, netbox, logger, model, data, dr=False, parent=None):

        assert (parent == None) or isinstance(parent, Upsert)
        assert isinstance(data, dict)

        self.netbox = netbox
        self.logger = logger
        self.model = model
        self.data = data
        self.dr = dr
        self.ref = netbox.nbcli.ref.get(model.split(':')[0])
        self.kwargs = dict()

        assert self.ref

        self.obj = self.action()

    def action(self):
        pass

    def proc_model(self):
    
        if '@' in self.model:
            self.model, up_ref = self.model.split('@', 1)
            self._update_ref(up_ref.split('@')[0])

        if ':' in self.model:
            self.model, kws = self.model.split(':', 1)
            kwlist = kws.split(':')
            for kw in kwlist:
                if '=' in kw:
                    proc_kw_str(self.kwargs, kw)
                else:
                    proc_kw_str(self.kwargs, '{}={}'.format(self.ref.lookup, kw))

    def _update_ref(self, string):
        pass


class Create(Upsert):
    pass


class Update(Upsert):
    pass


def store(netbox, logger, model, data, dr=False, parent=None):

    action = None

    if isinstance(data, dict):
        action = Update
        data = [data]
    elif isinstance(data, list):
        action = Create
    for obj in data:
        action(netbox, logger, model, obj, dr=False, parent=None)


class CreateSubCommand(BaseSubCommand):
    """This docstring will automatically be used as the command description.

    You can override this behavior by setting a description
    in the parser_kwargs dict.
    """

    name = 'create'
    parser_kwargs = dict(help='Create/Update objects with YAML file.')

    def setup(self):

        self.parser.add_argument('file',
                                 type=str,
                                 help='YAML file.')
        self.parser.add_argument('--dr', '--dry-run',
                                 action='store_true',
                                 help='Dry run.')

    def run(self):
        """This docstring will automatically be used as the command epilog.

        You can override this behavior by setting an epilog
        in the parser_kwargs dict.

        usage:
            nbcli hello --name John
        """

        with open(self.args.file) as fh:
            data = yaml.safe_load(fh.read())

        assert isinstance(data, dict)
        for key, value in data.items():
            assert self.netbox.nbcli.ref.get(key.split(':')[0])
            store(self.netbox, self.logger, key, value, dr=self.args.dr, parent=None)
