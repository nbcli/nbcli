import argparse
from pathlib import Path
from pydoc import getdoc
import sys
from textwrap import dedent
from nbcli import logger
from nbcli.core.extend import load_extensions
from nbcli.commands.base import BaseSubCommand


def main():
    """Command Line Interface for Netbox."""

    epilog='''
           General Options:
             -h, --help           show this help message and exit
             -v, --verbose        Show more logging messages
             -q, --quiet          Show fewer logging messages'''


    parser = argparse.ArgumentParser(prog='nbcli',
                                     description=dedent(getdoc(main)),
                                     epilog=dedent(epilog),
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.set_defaults(func=None)

    if 'init' not in sys.argv:
        load_extensions()

    subparsers = parser.add_subparsers(title='Commands',
                                       metavar='<command>')

    for command in BaseSubCommand.__subclasses__():
        command(subparsers)

    args = parser.parse_args()

    if args.func:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
