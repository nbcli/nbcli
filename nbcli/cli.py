import argparse
from .sub_commands import add_subcommands
from .sub_commands.base import BaseSubCommand

def main():

    parser = argparse.ArgumentParser(prog='nbcli')
    parser.set_defaults(func=None)

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-c', '--config', help='config file to use')
    common_parser.add_argument("-v", "--verbose",
                        	   action="count",
                        	   help="Show more logging messages")
    common_parser.add_argument("-q", "--quiet",
                        	   action="count",
                       		   help="Show fewer logging messages")

    subparsers = parser.add_subparsers(title='Commands',
                                       help='-h additional help',
                                       metavar='<command>')

    for command in BaseSubCommand.__subclasses__():
        command(subparsers, parents=[common_parser])

#    add_subcommands(subparsers, common_parser, view_parser)

    args = parser.parse_args()
#    print(args)
    if args.func:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
