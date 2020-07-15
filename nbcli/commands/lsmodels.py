import concurrent.futures
from pynetbox.core.query import Request
from nbcli.commands.base import BaseSubCommand


class LsmodelsSubCommand(BaseSubCommand):
    """Poll Netbox instance and list avaiable models."""

    name = 'lsmodels'
    parser_kwargs = dict(help='List Netbox Models')

    def run(self):
        """Poll Netbox instance and list available models.

        example usage:
          $ nbcli lsmodels"""

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
                    result.append('  ' + app + '.' + model.replace('-', '_'))
            return '\n'.join(result)

        if self.netbox.threading:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = executor.map(get_models, apps.items())
                [print(result) for result in results]
        else:
            for item in apps.items():
                print(get_models(item))
