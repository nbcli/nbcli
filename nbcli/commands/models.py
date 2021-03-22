"""Sub Command to set up bare nbcli user directory."""

from nbcli.commands.base import BaseSubCommand
from nbcli.core.utils import app_model_by_loc, rend_table
from nbcli.views.tools import view_name


class ModelsSubCommand(BaseSubCommand):
    """View Information on nbcli Models."""

    name = 'models'
    parser_kwargs = dict(help='Display information on Supported Models.')

    def setup(self):
        """Additional arguments for model command."""
        self.parser.add_argument('model',
                                 nargs='?',
                                 help='Display detailed info on given model.')

    def run(self):
        """View Information on nbcli Models.

        Example Usage:

        - List all supported models
          $ nbcli models

        - Show information of device model
          $ nbcli models device
        """
        if not self.args.model:

            header = ['Model', 'Lookup', 'Endpoint']

            table = [header]

            for res in self.netbox.nbcli.rm:
                loc = res.model.replace('.', '/').replace('_', '-')
                row = [res.alias, res.lookup, loc]
                table.append(row)

            print(rend_table(table))

        else:

            res = self.netbox.nbcli.rm.get(self.args.model)
            if res:
                ep = app_model_by_loc(self.netbox, res.model)

                disp = f'\nModel: {res.alias}\n' + \
                       f'Lookup: {res.lookup}\n' + \
                       f'View Name: {view_name(ep)}\n' + \
                       f'API Endpoint: {ep.url}\n'

                print(disp)

            else:
                self.logger.warning("Unsupported model: '%s'",
                                    self.args.model)
