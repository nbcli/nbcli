from ..core import get_session

def init_nbcli(args):
    get_session(conf_file=args.config, init=True)

def add_init(subparsers):
    parser_init = subparsers.add_parser('init', help='Initialize nbcli')
    parser_init.set_defaults(func=init_nbcli)
