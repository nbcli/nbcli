import argparse
from pathlib import Path
from pydoc import getdoc
import sys
from textwrap import dedent
from nbcli import logger
from nbcli.core.extend import load_extensions
from nbcli.commands.base import BaseSubCommand


class CLI():
    """Command Line Interface for Netbox."""

    def __init__(self):
        epilog='''
               General Options:
                 -h, --help           show this help message and exit
                 -v, --verbose        Show more logging messages
                 -q, --quiet          Show fewer logging messages'''


        self.parser = argparse.ArgumentParser(prog='nbcli',
                                     description=dedent(getdoc(main)),
                                     epilog=dedent(epilog),
                                     formatter_class=argparse.RawTextHelpFormatter)
        self.parser.set_defaults(func=None)

        if 'init' not in sys.argv:
            load_extensions()

        subparsers = self.parser.add_subparsers(title='Commands',
                                       metavar='<command>')

        for command in BaseSubCommand.__subclasses__():
            command(subparsers)

    def run(self, argv):

        args = self.parser.parse_args(argv)

        if args.func:
            args.func(args)
        else:
            self.parser.print_help()

def main():
    app = CLI()
    app.run(sys.argv[1:])

if __name__ == '__main__':
    main()
