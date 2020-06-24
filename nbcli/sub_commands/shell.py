import pkgutil
import sys
import requests
import pynetbox
from .base import BaseSubCommand

class Shell():

    def __init__(self, netbox, interactive_shell=None, script=None, interact=False):

        if pkgutil.find_loader('IPython') is None:
            interactive_shell = 'python'

        self.interactive_shell = interactive_shell
        self.script = script
        self.interact = interact
        self.netbox = netbox
        self.build_ns() 
        self.banner = ''
        self.banner += 'NetBox version {}\n'.format(self.netbox.version)
        self.banner += 'pynetbox version {}\n'.format(pynetbox.__version__)
        self.banner += 'Run lsnb() to view available pynetbox objects.\n'


    def build_ns(self):
        apps = ['Circuits',
                'DCIM',
                'Extras',
                'IPAM',
                'Secrets',
                'Tenancy',
                'Virtualization']

        self.ns = dict(Netbox=self.netbox)
        nbvars = dict(Netbox=dict())

        for app in apps:
            nbvars['Netbox'][app] = list()
            appobj = getattr(self.netbox, app.lower())
            self.ns[app] = appobj
            for endpoint in requests.get(self.netbox.base_url+'/'+app.lower(),
                                         verify=False).json().keys():
                if endpoint[0] != '_':
                    endpointname = endpoint.title().replace('-', '')
                    endpointobj = getattr(appobj, endpoint.replace('-', '_'))
                    if app == 'Virtualization' and endpoint == "interfaces":
                        endpointname = 'VirtualInterfaces'
                    nbvars['Netbox'][app].append(endpointname)
                    self.ns[endpointname] = endpointobj
        
        self.ns['nbvars'] = nbvars

        def lsnb():
            for api in nbvars.keys():
                print(api + ':')
                for app in nbvars[api].keys():
                    print('  ' + app + ":")
                    for ep in nbvars[api][app]:
                        print('    ' + ep)

        self.ns['lsnb'] = lsnb

    def python(self):
        from code import interact, InteractiveConsole
        banner = '\nPython version {}\n'.format(sys.version) + self.banner
        console = InteractiveConsole(locals=self.ns)
        if self.script:
            console.runcode(open(self.script).read())
            if self.interact:
                console.interact(banner='')
        else:
            console.interact(banner=banner)
    
    def ipython(self):
        from IPython import start_ipython
        from traitlets.config.loader import Config
    
        c = Config()
        c.TerminalInteractiveShell.banner2 = self.banner
        argv=[]

        if self.script:
            if self.interact:
                c.TerminalInteractiveShell.banner1 = ''
                c.TerminalInteractiveShell.banner2 = ''
                argv.append('-i')
            argv.append(self.script)

        start_ipython(argv=argv, user_ns=self.ns, config=c)
    
    def run(self):
        if self.interactive_shell == 'ipython':
            self.ipython()
        else:
            self.python()


class ShellSubCommand(BaseSubCommand):

    name = 'shell'
    parser_kwargs = dict(help='Launch interactive shell')

    def setup(self):

        self.parser.add_argument('script', nargs='?', type=str, help='Script to run')
        self.parser.add_argument('-i', action='store_true',
                      help='inspect interactively after running script')
        self.parser.add_argument('-s', '--interactive-shell', choices=['python', 'ipython'],
                      default='ipython',
                      help='Specifies interactive shell to use')

    def run(self):
 
        shell = Shell(self.netbox,
                      interactive_shell=self.args.interactive_shell,
                      script=self.args.script,
                      interact=self.args.i)
        shell.run()
