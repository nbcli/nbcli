from .base import BaseSubCommand, ProcKWArgsAction
from ..core import endpoint_by_loc
from ..views.tools import nbprint


class ShowSubCommand(BaseSubCommand):

    name = 'show'
    parser_kwargs = dict(help='Show detail view of Netbox Object')

    def setup(self):

        self.parser.add_argument('endpoint',
                                 type=str,
                                 help='Endpoint location to search')

        self.parser.add_argument('args',
                            nargs='+',
                            action=ProcKWArgsAction,
                            help='Search argumnets')


    def run(self):
        
        self.nbprint = nbprint

        ep = endpoint_by_loc(self.netbox, self.args.endpoint)
        result = ep.get(*self.args.args, **self.args.args_kwargs)
        if result:
            self.nbprint(result, view='detail')
        else:
            self.logger.warning('No results found')
