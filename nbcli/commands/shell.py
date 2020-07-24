from concurrent.futures import ThreadPoolExecutor
import pkgutil
import sys
import pynetbox
from pynetbox.core.endpoint import Endpoint
from pynetbox.core.response import Record
from pynetbox.core.query import Request
from nbcli.commands.base import BaseSubCommand
from nbcli.core.utils import app_model_loc
from nbcli.views.tools import nbprint, get_view_name

class Shell():

    def __init__(self, netbox,
                 interactive_shell=None,
                 script=None,
                 cmd=None,
                 interact=False,
                 skip_models=False,
                 logger=None):

        if pkgutil.find_loader('IPython') is None:
            interactive_shell = 'python'

        self.interactive_shell = interactive_shell
        self.script = script
        self.cmd = cmd
        self.interact = interact
        self.netbox = netbox
        self.logger = logger
        self.banner = ''
        versions = 'Python {}.{}.{} | NetBox {} | pynetbox {}'
        self.banner += versions.format(*sys.version_info[:3],
                                       self.netbox.version,
                                       pynetbox.__version__)
        self.banner += '\nAdditional utilities available:\n\t'
        self.build_ns(skip_models=skip_models) 


    def build_ns(self, skip_models=False):

        self.ns = dict(Netbox=self.netbox)
        if self.logger:
            self.ns['nblogger'] = self.logger
            self.banner += 'nblogger, '

        def load_models(item):
            app, url = item
            appobj = getattr(self.netbox, app)
            models = Request(url, self.netbox.http_session).get()
            for model in models.keys():
                if model[0] != '_':
                    modelname = model.title().replace('-', '')
                    modelobj = getattr(appobj, model.replace('-', '_'))
                    if app == 'virtualization' and model == "interfaces":
                        modelname = 'VirtualInterfaces'
                    self.ns[modelname] = modelobj

        if not skip_models:
            apps = Request(self.netbox.base_url, self.netbox.http_session).get()

            # for now only get apps pynetbox supports
            for app in list(apps.keys()):
                if not hasattr(self.netbox, app):
                    del apps[app]

            if self.netbox.threading:
                with ThreadPoolExecutor() as executor:
                    executor.map(load_models, apps.items())
            else:
                for item in apps.items():
                    load_models(item)

            nbns = dict(self.ns)

            def nbmodels(display='model'):
                """List available pynetbox models"""
                modeldict = dict()

                for key, value in nbns.items():
                    if isinstance(value, Endpoint):
                        app = value.url.split('/')[-2].title()
                        if app in modeldict.keys():
                            modeldict[app].append((key, value))
                        else:
                            modeldict[app] = list()
                            modeldict[app].append((key, value))

                for app, modellist in sorted(modeldict.items()):
                    print(app + ':')
                    for model in sorted(modellist):
                        if display == 'loc':
                            obj = Record({}, model[1].api, model[1])
                            print('  ' + app_model_loc(obj))
                        elif display == 'view':
                            obj = Record({}, model[1].api, model[1])
                            print('  ' + get_view_name(obj))
                        else:
                            print('  ' + model[0])

            self.ns['nbmodels'] = nbmodels
            self.banner += 'nbmodels(), '

        self.ns['nbprint'] = nbprint
        self.banner += 'nbprint()'


    def python(self):
        from code import interact, InteractiveConsole

        try:
            import readline
            import rlcompleter
            readline.set_completer(rlcompleter.Completer(self.ns).complete)
            readline.parse_and_bind('tab:complete')
        except:
            pass

        console = InteractiveConsole(locals=self.ns)
        if self.cmd:
            console.runcode(self.cmd)
        elif self.script:
            console.runcode(open(self.script).read())
            if self.interact:
                console.interact(banner='')
        else:
            console.interact(banner=self.banner)
    
    def ipython(self):
        from IPython import start_ipython, __version__
        from traitlets.config.loader import Config
    
        banner = 'IPython {} | '.format(__version__) + self.banner

        c = Config()
        c.TerminalInteractiveShell.banner1 = banner
        argv=[]
        if self.cmd:
            argv.append('-c')
            argv.append(self.cmd)
        elif self.script:
            if self.interact:
                c.TerminalInteractiveShell.banner1 = ''
                argv.append('-i')
            argv.append(self.script)

        start_ipython(argv=argv, user_ns=self.ns, config=c)
    
    def run(self):
        if self.interactive_shell == 'ipython':
            self.ipython()
        else:
            self.python()


class ShellSubCommand(BaseSubCommand):
    """Launch Interactive Shell with pynetbox objects preloaded."""

    name = 'shell'
    parser_kwargs = dict(help='Launch interactive shell')

    def setup(self):

        self.parser.add_argument('script', nargs='?', type=str, help='Script to run')
        self.parser.add_argument('-c', metavar='cmd', type=str, help='Program passed in as string')
        self.parser.add_argument('-i', action='store_true',
                      help='inspect interactively after running script')
        self.parser.add_argument('-s', '--interactive-shell', choices=['python', 'ipython'],
                      default='ipython',
                      help='Specifies interactive shell to use')
        self.parser.add_argument('--skip',
                                 action='store_true',
                                 help='Skip loading models.')

    def run(self):
        """Run Shell enviornment.

        Example usage:
        $ nbcli shell -i myscript.py
        $ nbcli shell -s python"""
 
        shell = Shell(self.netbox,
                      interactive_shell=self.args.interactive_shell,
                      script=self.args.script,
                      cmd=self.args.c,
                      interact=self.args.i,
                      skip_models=self.args.skip,
                      logger=self.logger)
        shell.run()
