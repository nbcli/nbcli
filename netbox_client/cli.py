import argparse
from .core import get_session

def init(args):
    get_session(conf_file=args.config, init=True)

def main():

    parser = argparse.ArgumentParser(description='nbcli', prog='nbcli')
    parser.set_defaults(func=None)
    parser.add_argument('-c', '--config', default='.netbox-client.ini',
                        help='config file to use')

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_init = subparsers.add_parser('init', help='Initialize netbox-client')
    parser_init.set_defaults(func=init)

    args = parser.parse_args()
    print(args)
    if args.func:
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
