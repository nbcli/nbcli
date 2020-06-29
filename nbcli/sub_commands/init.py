import logging
from .base import BaseSubCommand
from ..core import get_session

class InitSubCommand(BaseSubCommand):
    """Initialize nbcli.

    Default confg directory location $HOME/.nbcli.d
    After running edit $HOME/.nbcli.d/config.py with your credentials."""

    name = 'init'
    parser_kwargs = dict(help='Initialize nbcli.')

    def _pre_run_(self, args):
        
        self.args = args
        self.logger = logging.getLogger('nbcli.'+self.name)
        self._set_log_level_()
        self.logger.debug(args)
        self.run()

    def run(self):
        """Create nbcli config directory and related files.

        example usage:
        $ nbcli init
        $ nbcli init --conf_dir .alt_nbcli.d"""

        self.netbox = get_session(conf_file=self.args.conf_dir, init=True)
