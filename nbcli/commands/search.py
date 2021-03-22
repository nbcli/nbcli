"""Search sub command to emulate Netbox main search bar."""


from pynetbox.core.query import Request
from pynetbox.core.endpoint import response_loader
from nbcli.commands.base import BaseSubCommand
from nbcli.core.utils import app_model_by_loc
from nbcli.views.tools import nbprint


class SearchSubCommand(BaseSubCommand):
    """Search Netbox objects with the given searchterm.

    The List of search models can be modified in:
    $HOME/$CONF_DIR/config.py
    """

    name = 'search'
    parser_kwargs = dict(help='Search Netbox Objects')

    def setup(self):
        """Add parser arguments to search sub command."""
        self.parser.add_argument('app_model',
                                 type=str,
                                 nargs='?',
                                 help='Model location to search (app.model)')

        self.parser.add_argument('searchterm',
                                 help='Search term')

    def run(self):
        """Run a search of Netbox objects and show a table view of results.

        Usage Examples:

        - Search all search modelss for 'server1':
          $ nbcli search server1

        - Search the dcim.interfaces model for 'eth 1':
          $ nbcli search interface 'eth 1'
        """
        if hasattr(self.netbox.nbcli.conf, 'nbcli') and \
                ('search_models' in self.netbox.nbcli.conf.nbcli.keys()):
            self.search_models = self.netbox.nbcli.conf.nbcli['search_models']
        else:
            self.search_models = ['provider',
                                  'circuit',
                                  'site',
                                  'rack',
                                  'rack_group',
                                  'device_type',
                                  'device',
                                  'virtual_chassis',
                                  'cable',
                                  'power_feed',
                                  'vrf',
                                  'aggregate',
                                  'prefix',
                                  'address',
                                  'vlan',
                                  'secret',
                                  'tenant',
                                  'cluster',
                                  'virtual_machine']

        def search(ep):
            req = Request(filters=dict(q=self.args.searchterm),
                          base=ep.url,
                          token=ep.token,
                          session_key=ep.session_key,
                          http_session=ep.api.http_session)

            rep = req._make_call(add_params=dict(limit=15))

            result = list()

            if rep.get('results'):
                result = response_loader(rep['results'], ep.return_obj, ep)

            return result

        self.nbprint = nbprint

        if self.args.app_model:
            modellist = [self.args.app_model]
        else:
            modellist = self.search_models

        result_count = 0

        print('')
        for app_model in modellist:
            model = app_model_by_loc(self.netbox, app_model)
            result = search(model)
            full_count = model.count(self.args.searchterm)
            if len(result) > 0:
                result_count += 1
                print('{}\n{}'.format(app_model.title(), '=' * len(app_model)))
                self.nbprint(result)
                if len(result) < full_count:
                    print('*** See all {} results: '.format(full_count) +
                          "'$ nbcli filter {} {}' ***".
                          format(app_model, self.args.searchterm))
                print('')
        if result_count == 0:
            self.logger.warning('No results found')
            print('')
