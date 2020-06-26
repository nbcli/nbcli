from .base import BaseSubCommand
from ..core import endpoint_by_loc
from ..views.tools import nbprint

SEARCH_ENDPOINTS = ['circuits.providers',
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

    name = 'search'
    parser_kwargs = dict(help='Search Netbox Objects')

    def setup(self):

        self.parser.add_argument('endpoint',
                                 type=str,
                                 nargs='?',
                                 help='Endpoint location to search')

        self.parser.add_argument('searchterm',
                                 type=str,
                                 help='Search term')

    def run(self):
        
        self.nbprint = nbprint

        print('')
        if self.args.endpoint:
            ep = endpoint_by_loc(self.netbox, self.args.endpoint)
            result = ep.filter(self.args.searchterm)
            if len(result) > 0:
                endpoint = self.args.endpoint.lower().replace('-', '_')
                print('# Endpoint:', endpoint)
                self.nbprint(result)
            else:
                self.logger.warning('No results found')
            print('')
        else:
            result_count = 0
            for endpoint in SEARCH_ENDPOINTS:
                ep = endpoint_by_loc(self.netbox, endpoint)
                result = ep.filter(self.args.searchterm)
                if len(result) > 0:
                    result_count += 1
                    print('# Endpoint:', endpoint)
                    self.nbprint(result)
                    print('')
            if result_count == 0:
                self.logger.warning('No results found')
                print('')
