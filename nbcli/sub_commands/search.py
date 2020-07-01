from .base import BaseSubCommand, ProcKWArgsAction
from ..core import app_model_by_loc
from ..views.tools import nbprint

SEARCH_MODELS = ['circuits.providers',
                    'circuits.circuits',
                    'dcim.sites',
                    'dcim.racks',
                    'dcim.rack_groups',
                    'dcim.device_types',
                    'dcim.devices',
                    'dcim.virtual_chassis',
                    'dcim.cables',
                    'dcim.power_feeds',
                    'ipam.vrfs',
                    'ipam.aggregates',
                    'ipam.prefixes',
                    'ipam.ip_addresses',
                    'ipam.vlans',
                    'secrets.secrets',
                    'tenancy.tenants',
                    'virtualization.clusters',
                    'virtualization.virtual_machines']


class SearchSubCommand(BaseSubCommand):
    """Search Netbox objects with the given searchterm.

    The List of search models can be modified in:
    $HOME/$CONF_DIR/config.py"""

    name = 'search'
    parser_kwargs = dict(help='Search Netbox Objects')

    def setup(self):

        self.parser.add_argument('app_model',
                                 type=str,
                                 nargs='?',
                                 help='Model location to search (app.model)')

        self.parser.add_argument('searchterm',
                            help='Search term')

    def run(self):
        """Run a search of Netbox objects and show a table view of results.

        example usage:
        - search all search modelss for 'server1':
          $ nbcli search server1
        - search the dcim.interfaces model for 'eth 1':
          $ nbcli search dcim.interfaces 'eth 1'"""

        self.nbprint = nbprint

        print('')
        if self.args.app_model:
            model = app_model_by_loc(self.netbox, self.args.app_model)
            result = model.filter(self.args.searchterm)
            if len(result) > 0:
                app_model = self.args.app_model.lower().replace('-', '_')
                print('# Model:', app_model)
                self.nbprint(result)
            else:
                self.logger.warning('No results found')
            print('')
        else:
            result_count = 0
            for app_model in SEARCH_MODELS:
                model = app_model_by_loc(self.netbox, app_model)
                result = model.filter(self.args.searchterm)
                if len(result) > 0:
                    result_count += 1
                    print('# Model:', app_model)
                    self.nbprint(result)
                    print('')
            if result_count == 0:
                self.logger.warning('No results found')
                print('')
