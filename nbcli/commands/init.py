import logging
from nbcli.commands.base import BaseSubCommand
from nbcli.core.config import get_session

class InitSubCommand(BaseSubCommand):
    """Initialize nbcli.

    Default confg directory location $HOME/.nbcli
    After running edit $HOME/.nbcli/user_config.yml with your credentials."""

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

        Example Usage:

        - Initialize nbcli
          $ nbcli init
        """

        self.netbox = get_session(init=True)
