from nbcli.commands.base import BaseSubCommand, ProcKWArgsAction
from nbcli.core.utils import app_model_by_loc
from nbcli.views.tools import nbprint


class ShowSubCommand(BaseSubCommand):

    name = 'show'
    parser_kwargs = dict(help='Show detail view of Netbox Object')

    def setup(self):

        self.parser.add_argument('app_model',
                                 type=str,
                                 help='Model location to search (app.model)')

        self.parser.add_argument('args',
                            nargs='+',
                            action=ProcKWArgsAction,
                            help='Search argumnets')


    def run(self):
        
        self.nbprint = nbprint

        ep = app_model_by_loc(self.netbox, self.args.app_model)
        result = ep.get(*self.args.args, **self.args.args_kwargs)
        if result:
            self.nbprint(result, view='detail')
        else:
            self.logger.warning('No results found')
