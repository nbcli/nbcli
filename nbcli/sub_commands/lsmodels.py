import concurrent.futures
#import requests
from .base import BaseSubCommand
from ..core.utils import get_req


class LsmodelsSubCommand(BaseSubCommand):
    """Poll Netbox instance and list avaiable models."""

    name = 'lsmodels'
    parser_kwargs = dict(help='List Netbox Models')

    def run(self):
        """Poll Netbox instance and list available models.

        example usage:
          $ nbcli lsmodels"""

        apps = get_req(self.netbox, self.netbox.base_url)

        def get_models(item):
            app, url = item
            result = list()
            result.append(app.title() + ':')
            models = get_req(self.netbox, url)
            for model in models.keys():
                if model[0] != '_':
                    result.append('  ' + app + '.' + model.replace('-', '_'))
            return '\n'.join(result)

        if self.netbox.threading:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(get_models, apps.items())
                [print(result) for result in results]
        else:
            for item in apps.items():
                print(get_models(item))
