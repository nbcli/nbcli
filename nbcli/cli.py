import argparse
from .sub_commands.base import BaseSubCommand

def main():

    parser = argparse.ArgumentParser(prog='nbcli')
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(title='Commands',
                                       help='-h additional help',
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
