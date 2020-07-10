import argparse
from pathlib import Path
from pydoc import getdoc
import sys
from textwrap import dedent
from nbcli import logger
from nbcli.core.extend import load_extensions
from nbcli.sub_commands.base import BaseSubCommand


load_extensions()

#sys.path.append(str(Path.home().joinpath('.nbcli').joinpath('user_extensions')))
#try:
#    import user_views
#except:
#    print('Error loading user_views')
#try:
#    import user_commands
#except Exception as e:
#    print(e)

def main():
    """Command Line Interface for Netbox."""

    epilog='''
           General Options:
             -h, --help           show this help message and exit
             --conf_dir CONF_DIR  Specify config directory
             -v, --verbose        Show more logging messages
             -q, --quiet          Show fewer logging messages'''


    parser = argparse.ArgumentParser(prog='nbcli',
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
