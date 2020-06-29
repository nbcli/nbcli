import argparse
import logging
from pydoc import getdoc
from textwrap import dedent
from .sub_commands.base import BaseSubCommand

def main():
    """Command Line Interface for Netbox."""

    epilog='''
           General Options:
             -h, --help           show this help message and exit
             --conf_dir CONF_DIR  Specify config directory
             -v, --verbose        Show more logging messages
             -q, --quiet          Show fewer logging messages'''

    logging.basicConfig(format="[%(levelname)s](%(name)s): %(message)s")

    parser = argparse.ArgumentParser(prog='nbcli',
                                     usage='nbcli <command> [options]',
                                     description=dedent(getdoc(main)),
                                     epilog=dedent(epilog),
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.set_defaults(func=None)

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
