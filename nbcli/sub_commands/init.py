import logging
from .base import BaseSubCommand
from ..core import get_session

class InitSubCommand(BaseSubCommand):

    name = 'init'
    parser_kwargs = dict(help='Initialize nbcli.')

    def _pre_run_(self, args):
        
        self.args = args
        self.netbox = get_session(conf_file=args.config, init=True)
        self.logger = logging.getLogger('nbcli.'+self.name)
        self.run()
