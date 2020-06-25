import argparse
import logging
import sys
from .sub_commands.base import BaseSubCommand

def main():

    logging.basicConfig(format="[%(levelname)s](%(name)s): %(message)s")

    parser = argparse.ArgumentParser(prog='nbcli')
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(title='Commands',
                                       help='-h additional help',
                                       metavar='<command>')

    for command in BaseSubCommand.__subclasses__():
        command(subparsers)

    args = parser.parse_args()

    try:
        if args.func:
            args.func(args)
        else:
            parser.print_help()
    except Exception as e:
        print(type(e).__name__)
        print(e)
        raise e

        sys.exit(1)

if __name__ == '__main__':
    main()
