import pkgutil
import sys
import pynetbox
from pynetbox.core.endpoint import Endpoint
from pynetbox.core.response import Record
from pynetbox.core.query import Request
from nbcli.commands.base import BaseSubCommand
from nbcli.core.utils import app_model_loc, app_model_by_loc
from nbcli.views.tools import nbprint

class Shell():

    def __init__(self, netbox,
                 interactive_shell=None,
                 script=None,
                 cmd=None,
                 interact=False,
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
        self.build_ns() 


    def build_ns(self):

        self.ns = dict(Netbox=self.netbox,
                       nblogger=self.logger,
                       nbprint=nbprint)
        self.banner += 'nbprint(), nblogger'

        for res in self.netbox.nbcli.rm:
            name = res.alias.title().replace('_', '')
            self.ns[name] = app_model_by_loc(self.netbox, res.model)


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
                      logger=self.logger)
        shell.run()
