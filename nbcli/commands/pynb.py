from pynetbox.core.response import Record
from nbcli.commands.base import BaseSubCommand, ProcKWArgsAction
from nbcli.core.utils import app_model_by_loc


class Pynb():

    ep_methods = ('all', 'choices', 'count', 'create', 'filter', 'get')

    def __init__(self,
                 netbox,
                 endpoint,
                 method,
                 args=list(),
                 kwargs=dict(),
                 delete=False,
                 update=list(),
                 update_kwargs=dict(),
                 de=list(),
                 dea=list(),
                 dea_kwargs=dict()):

        assert method in self.ep_methods, \
            'Allowed methods ' + str(self.ep_methods)

        self.endpoint = app_model_by_loc(netbox, endpoint)
        self.method = getattr(self.endpoint, method)

        if method == 'create':
            # TODO json.loads(args) and pass to create
            result = self.method(**kwargs)
        else:
            result = self.method(*args, **kwargs)

        if (method == 'get') and isinstance(result, Record):
            if delete:
                self.delete(result)
            elif update or update_kwargs:
                self.update(result, *update, **update_kwargs)
            elif de:
                self.detail(result, de[0], de[1], *dea, **dea_kwargs)
            else:
                self.result = result
        else:
            self.result = result

    def delete(self, obj):
        ans = input('Delete {}: ({}) {}? '.format(obj.__class__.__name__,
                                                  str(obj.id),
                                                  str(obj)))
        if ans.lower() == 'yes':
            if obj.delete():
                self.result = 'Deleted'
            else:
                self.result = 'Error deleting'
        else:
            self.result = '{}: {} not deleted!'.format(obj.__class__.__name__,
                                                       str(obj))

    def update(self, obj, *args, **kwargs):
        # TODO: json.loads(args) and pass to update 
        self.result = obj.update(kwargs)

    def detail(self, obj, detail, method, *args, **kwargs):
        de = getattr(obj, detail)
        self.result = getattr(de, method)(*args, **kwargs)


class PynbSubCommand(BaseSubCommand):

    name = 'pynb'
    parser_kwargs = dict(help='Wrapper for pynetbox')
    view_options = True


    def setup(self):
    
        self.parser.add_argument('endpoint',
                            help="App endpoint")
    
        self.parser.add_argument('method',
                            help="Endpoint Method")
    
        self.parser.add_argument('args',
                            nargs='*',
                            action=ProcKWArgsAction,
                            help='Argumnet to pass to func')
    
        obj_meth = self.parser.add_mutually_exclusive_group()
    
        obj_meth.add_argument('-D', '--delete',
                              action='store_true',
                              help='Delete Object retrieved by get method')
    
        obj_meth.add_argument('-u', '--update',
                              metavar='UD-ARGS',
                              nargs='+',
                              action=ProcKWArgsAction,
                              help='Update object with given kwargs')
    
        obj_meth.add_argument('--de', '--detail-endpoint',
                              metavar=('DE', 'DE-METHOD'),
                              nargs=2,
                              help='Get the detail endpoint of object')
    
        self.parser.add_argument('--dea', '--de-args',
                            metavar='DE-ARGS',
                            nargs='*',
                            action=ProcKWArgsAction,
                            help='Argumets to pass to the de-action')


    def run(self):
    
        if self.args.update is None:
            self.args.update = list()
            self.args.update_kwargs = dict()
    
        if self.args.de is None:
            self.args.de = list()
    
        if self.args.dea is None:
            self.args.dea = list()
            self.args.dea_kwargs = dict()

        cli = Pynb(self.netbox,
                   self.args.endpoint,
                   self.args.method,
                   args=self.args.args,
                   kwargs=self.args.args_kwargs,
                   delete=self.args.delete,
                   update=self.args.update,
                   update_kwargs=self.args.update_kwargs,
                   de=self.args.de,
                   dea=self.args.dea,
                   dea_kwargs=self.args.dea_kwargs)
        if cli.result:
            self.nbprint(cli.result, cols=self.args.cols)
        else:
            self.logger.warning('No results found')
