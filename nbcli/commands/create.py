import yaml
from nbcli.core.utils import app_model_by_loc
from nbcli.commands.base import BaseSubCommand, proc_kw_str


def resolve_ref(netbox, kwargs, key, value, create=False):
    ref = netbox.nbcli.ref.get(key)
    if ref.answer == ref.lookup:
        proc_kw_str(kwargs, '{}={}'.format(ref.hook, value))
        return
    ep = app_model_by_loc(netbox, ref.model)
    obj = ep.get(**{ref.lookup: value})
    if hasattr(obj, ref.answer):
        if create:
            proc_kw_str(kwargs, '{}={}'.format(ref.alias, getattr(obj, ref.answer)))
        else:
            proc_kw_str(kwargs, '{}={}'.format(ref.hook, getattr(obj, ref.answer)))
    else:
        netbox.nbcli.logger.warning('Could not resolve {}: {}, Skipping',
                                    key, value)


class Upsert():

    def __init__(self, netbox, logger, model, data,
                 dr=False,      # dry run
                 ud=False,      # update only
                 gp=True,       # ref parent hook on get request for update
                 parent=None):

        assert (parent == None) or isinstance(parent, Upsert)

        if isinstance(data, list):
            for d in data:
                Upsert(netbox, logger, model, d, dr=dr, ud=ud, gp=False, parent=parent)
            return

        self.netbox = netbox
        self.logger = logger
        self.model = model
        self.data = data
        self.dr = dr
        self.ud = ud
        self.gp = gp
        self.parent = parent
        self.ref = netbox.nbcli.ref.get(model.split(':')[0])
        self.kwargs = dict()
        self.get_kwargs = dict()
        self.children = list()  # list of tuples (model, data)

        assert self.ref

        self.obj = None

        self.proc_model()

        self.get()

        self.action()

        self.proc_children()

    def get(self):

        if self.get_kwargs:
            self.obj = self.model.get(**self.get_kwargs)
        if not self.obj:
            self.kwargs.update(self.get_kwargs)

    def action(self):
        
        if self.obj:
            for key, value in self.data.items():
                self.proc_data_items(key, value)
            self.logger.info('Updating %s with data: %s',
                             str(self.obj), str(self.kwargs))
            self.obj.update(self.kwargs)
        else:
            for key, value in self.data.items():
                self.proc_data_items(key, value, create=True)
            self.logger.info('Creating %s with data: %s',
                             self.ref.alias, str(self.kwargs))
            self.obj = self.model.create(**self.kwargs)

    def proc_model(self):

        if self.model.endswith('^'):
            self.gp = False
            self.model = self.model[:-1]
    
        if '@' in self.model:
            self.model, up_ref = self.model.split('@', 1)
            self._update_ref(up_ref.split('@')[0])

        if ':' in self.model:
            self.model, kws = self.model.split(':', 1)
            kwlist = kws.split(':')
            for kw in kwlist:
                if '=' in kw:
                    proc_kw_str(self.get_kwargs, kw)
                else:
                    proc_kw_str(self.get_kwargs,
                                '{}={}'.format(self.ref.lookup, kw))

        if self.parent:
            d = dict()
            d[self.parent.ref.hook] = getattr(self.parent.obj,
                                              self.parent.ref.answer)

            if self.get_kwargs and self.gp:
                self.get_kwargs.update(d)
            else:
                self.kwargs.update(d)

        self.model = app_model_by_loc(self.netbox, self.model)

    def proc_data_items(self, key, value, create=False):

        if self.netbox.nbcli.ref.get(key.split(':')[0]):
            if  (':' in key) and (value is None):
                self.children.append((key, {}))
            elif isinstance(value, (dict, list)):
                self.children.append((key, value))
            else:
                resolve_ref(self.netbox, self.kwargs, key, value, create=create)
        else:
            self.kwargs[key] = value

    def proc_children(self):

        for child in self.children:

            model, data = child

            Upsert(self.netbox, self.logger, model, data,
                   dr=self.dr,
                   ud=self.ud,
                   parent=self)


    def _update_ref(self, string):
        pass


class CreateSubCommand(BaseSubCommand):
    """Create and/or Update objects defined in YAML file."""

    name = 'create'
    parser_kwargs = dict(help='Create/Update objects with YAML file.')

    def setup(self):

        self.parser.add_argument('file',
                                 type=str,
                                 help='YAML file.')
        self.parser.add_argument('--dr', '--dry-run',
                                 action='store_true',
                                 help='Dry run.')
        self.parser.add_argument('-u', '--update-only',
                                 action='store_true',
                                 help='Do not create object not found '+ \
                                      'with the lookup key schema.')

    def run(self):
        """Run command.

        See documentation for YAML file reference and examples.
        https://nbcli.readthedocs.io/en/release/create.html

        Usage Examples:

        - Create/Update objects defined in YAML file
          $ nbcli create file.yml
        """

        with open(self.args.file) as fh:
            data_stream = yaml.safe_load_all(fh.read())

        for data in data_stream:
            for key, value in data.items():
                assert self.netbox.nbcli.ref.get(key.split(':')[0])
                Upsert(self.netbox, self.logger, key, value,
                       dr=self.args.dr,
                       ud=self.args.update_only,
                       gp=False,
                       parent=None)
