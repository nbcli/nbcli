import sys
from pprint import pprint
from pynetbox.core.response import Record
from .base import BaseSubCommand, ProcKWArgsAction
from ..views.tools import display_result

ENDPOINT_METHODS = ('all', 'choices', 'count', 'create', 'filter', 'get')


class Pynb():

    def __init__(self,
                 netbox,
                 app,
                 endpoint,
                 method,
                 args=list(),
                 kwargs=dict(),
                 delete=False,
                 update=list(),
                 update_kwargs=dict(),
                 de=list(),
                 dea=list(),
                 dea_kwargs=dict(),
                 nbprint=print):

        assert method in ENDPOINT_METHODS, \
            'Allowed methods ' + str(ENDPOINT_METHODS)

        self.netbox = netbox
        self.nbprint = nbprint
        self.app = getattr(self.netbox, app)
        self.endpoint = getattr(self.app, endpoint)
        self.method = getattr(self.endpoint, method)
        self.result = self.method(*args, **kwargs)

    def display(self, header=True):

        if not self.result:
            print('No result to display')
        elif isinstance(self.result, int):
            print(self.result)
        elif isinstance(self.result, list):
            if (len(self.result) > 0) and isinstance(self.result[0], Record):
                display_result(self.result, header=header)
            else:
                for i in self.result:
                    print(i)
        elif isinstance(self.result, Record):
            display_result(self.result, header=header)
        else:
            print(self.result)

    def delete(self, obj):
        print('Not Implemented!')

    def update(self, obj):
        print('Not Implemented!')

    def detail(self, obj):
        print('Not Implemented!')


class PynbSubCommand(BaseSubCommand):

    name = 'pynb'
    parser_kwargs = dict(help='Wrapper for pynetbox')
    view_options = True

    def run(self):
    
        if self.args.update is None:
            self.args.update = list()
            self.args.update_kwargs = dict()
    
        if self.args.de is None:
            self.args.de = list()
    
        if self.args.dea is None:
            self.args.dea = list()
            self.args.dea_kwargs = dict()
    
        try:
            cli = Pynb(self.netbox,
                       self.args.app,
                       self.args.endpoint,
                       self.args.method,
                       args=self.args.args,
                       kwargs=self.args.args_kwargs,
                       delete=self.args.delete,
                       update=self.args.update,
                       update_kwargs=self.args.update_kwargs,
                       de=self.args.de,
                       dea=self.args.dea,
                       dea_kwargs=self.args.dea_kwargs,
                       nbprint=self.args.nbprint)
            cli.nbprint(cli.result)
            #cli.display(header=self.args.nh)
    
        except Exception as e:
            print(type(e).__name__)
            print(e)
            raise e
    
            sys.exit(1)
    
    
    def setup(self):
    
        self.parser.add_argument('app',
                            metavar="APP",
                            type=str,
                            help="App to call")
    
        self.parser.add_argument('endpoint',
                            metavar="ENDPOINT",
                            type=str,
                            help="App endpoint")
    
        self.parser.add_argument('method',
                            metavar="METHOD",
                            type=str,
                            choices=ENDPOINT_METHODS,
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
