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
        """Show Detail view of object.

        Usage Examples:

        - Show Site with id 1
          $ nbcli show dcim.sites 1

        - Show Device with name server01
          $ nbcli show dcim.devices name=server01

        - Show Prefix 10.1.1.0/24
          $ nbcli show ipam.prefixes prefix=10.1.1.0/24
        """
        self.nbprint = nbprint

        ep = app_model_by_loc(self.netbox, self.args.app_model)
        result = ep.get(*self.args.args, **self.args.args_kwargs)
        if result:
            self.nbprint(result, view='detail')
        else:
            self.logger.warning('No results found')
