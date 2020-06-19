import argparse
from .sub_commands import add_subcommands

def main():

    parser = argparse.ArgumentParser(description='nbcli', prog='nbcli')
    parser.set_defaults(func=None)
    parser.add_argument('-c', '--config', help='config file to use')

    subparsers = parser.add_subparsers(help='sub-command help')

    add_subcommands(subparsers)

    args = parser.parse_args()
    print(args)
    if args.func:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
