import concurrent.futures
import re
from pynetbox.core.query import Request
from nbcli.commands.base import BaseSubCommand


class NbmodelsSubCommand(BaseSubCommand):
    """Poll Netbox instance and list available models."""

    name = 'nbmodels'
    parser_kwargs = dict(help='List Netbox Models')

    def setup(self):

        self.parser.add_argument('--view-name',
                                 action='store_true',
                                 help='Display view name')

    def run(self):
        """Poll Netbox instance and list available models.

        Usage Examples:

        - List available NetBox models
          $ nbcli nbmodels

        - Show view names instead of models
          $ nbcli nbmodels --view-name
        """

        apps = Request(self.netbox.base_url, self.netbox.http_session).get()

        # for now only get apps pynetbox supports
        for app in list(apps.keys()):
            if not hasattr(self.netbox, app):
                del apps[app]

        def get_models(item):
            app, url = item
            result = list()
            result.append(app.title() + ':')
            models = Request(url, self.netbox.http_session).get()
            for model in models.keys():
                if model[0] != '_':
                    loc = app + '.' + model.replace('-', '_')
                    name = re.sub('\.|_', '', loc.title()) + 'View'

                    if self.args.view_name:
                        loc = name

                    result.append('  {}'.format(loc))

            return '\n'.join(result)

        if self.netbox.threading:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(get_models, apps.items())
                [print(result) for result in results]
        else:
            for item in apps.items():
                print(get_models(item))
