"""Sub Command to set up bare nbcli user directory."""

from nbcli.commands.base import BaseSubCommand
from nbcli.core.utils import app_model_by_loc, rend_table, get_nbcli_dir
from nbcli.views.tools import view_name

from nbcli import __version__ as nbcli_version
from pynetbox import __version__ as pynb_version

from os import environ


class InfoSubCommand(BaseSubCommand):
    """View Information about nbcli instance."""

    name = 'info'
    parser_kwargs = dict(help='Display information about nbcli instance.')

    def setup(self):
        """Additional arguments for info command."""

        info_opts = self.parser.add_mutually_exclusive_group()

        info_opts.add_argument('--detailed',
                               action='store_true',
                               help='Show more detailed info.')
        info_opts.add_argument('--models',
                               nargs='?',
                               default=None,
                               const='all',
                               help='Display detailed info on given model.')

    def run(self):
        """View Information about nblci instance.

        Example Usage:

        - Show version info
          $ nbcli info

        - Show more detailed info
          $ nbcli info --detailed

        - List all supported models
          $ nbcli info --models

        - Show information of device model
          $ nbcli info --models device
        """

        if self.args.models:
            if self.args.models == 'all':

                header = ['Model', 'Lookup', 'Endpoint']

                table = [header]

                for res in self.netbox.nbcli.rm:
                    loc = res.model.replace('.', '/').replace('_', '-')
                    row = [res.alias, res.lookup, loc]
                    table.append(row)

                print(rend_table(table))

            else:

                res = self.netbox.nbcli.rm.get(self.args.models)
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

        else:
            print(f'\nnbcli version: {nbcli_version}\n' + \
                  f'NetBox version: {self.netbox.version}\n' + \
                  f'pynetbox version: {pynb_version}\n')

            if self.args.detailed:
                print(f'nbcli dir: {get_nbcli_dir()}\n')

                nbcli_vars = {key:val for key, val in environ.items() if key.startswith('NBCLI_')}

                if len(nbcli_vars) > 0:
                    print('nbcli environment variables:')
                    for key, val in nbcli_vars.items():
                        print(f'\t{key}: {val}')
                    print()
