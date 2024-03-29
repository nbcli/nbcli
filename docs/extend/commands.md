# Custom Commands

## Example custom command

```python
# For a user defined subcommand to be loaded into nbcli
# it must be a subclass of BaseSubCommand, found in nbcli.commands.base

from nbcli.commands.base import BaseSubCommand

class ExampleSubCommand(BaseSubCommand):
    """This docstring will automatically be used as the command description.

    You can override this behavior by setting a description
    in the parser_kwargs dict.
    """

    # name is required

    name = 'hello'

    # parser_kwargs is optional 
    # It shoud be a dict containing values you with to pass to
    # the ArgumentParser for the command.
    # (see https://docs.python.org/3/library/argparse.html)
    # the value for 'help' will be displayed next to the command
    # when 'nbcli -h' is run

    parser_kwargs = dict(help='Say hello',
                         #description=None,
                         #epilog=None,
                         )

    # view_options is optional.
    # If True it will add --view, --view-model, --cols, and --nh arguments
    # to the command ArgumentParser and add a pre-configured nbprint() method
    # available in run()

    view_options = False

    def setup(self):

        # Any additional argument that need to be added to the command
        # ArgumentParser should be added here.
        # (see https://docs.python.org/3/library/argparse.html)

        self.parser.add_argument('--name',
                                 type=str,
                                 default='World',
                                 help='Who are you saying hello to?')

    def run(self):
        """This docstring will automatically be used as the command epilog.

        You can override this behavior by setting an epilog
        in the parser_kwargs dict.

        Usage Examples:

        - Say hello to the world
          $ nbcli hello

        - Say hello to John
          $ nbcli hello --name John
        """

        # self.netbox is the pre-configured root pynetbox api object
        # to be used to interact with the NetBox REST API
        # (see https://pynetbox.readthedocs.io/en/latest/)

        # self.args is the parsed arguments for the command
        # (see https://docs.python.org/3/library/argparse.html)

        # self.logger is a logger with a pre-set name/loglevel
        # set from parsed arguments
        # (see https://docs.python.org/3/library/logging.html)

        # self.nbprint will be added if view_options is set to True
        # otherwise it can be imported from nbcli.views.tools

        print('Hello, {}!'.format(self.args.name))
```
