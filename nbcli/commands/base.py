"""Base sub-command and tools for commands."""


import argparse
from argparse import RawTextHelpFormatter
import functools
import logging
import sys
from pydoc import getdoc
from textwrap import dedent
from nbcli.core.config import get_session
from nbcli.views.tools import nbprint


def get_common_parser():
    """Create parser for handling verbose options."""
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-v', '--verbose',
                               action='count',
                               help='Show more logging messages')
    common_parser.add_argument('-q', '--quiet',
                               action='count',
                               help='Show fewer logging messages')
    return common_parser


def get_view_parser():
    """Create parser for handling view options."""
    view_parser = argparse.ArgumentParser(add_help=False)
    view_parser.add_argument('--view', type=str, help='Output view.',
                             choices=['table', 'detail', 'json'],
                             default='table')
    view_parser.add_argument('--view-model',
                             type=str,
                             help='View model to use')
    view_parser.add_argument('--cols', nargs='*',
                             help="Custome columns for table output.")
    view_parser.add_argument('--nh', '--no-header',
                             action='store_true',
                             help='Disable header row in results')
    return view_parser


class BaseSubCommand():
    """Base sub-command to build commands from."""

    name = 'base'
    parser_kwargs = dict(help='')
    view_options = False
    default_loglevel = logging.WARNING

    def __init__(self, subparser):
        """Add sub-command parser to subparser object."""
        if 'parents' in self.parser_kwargs.keys():
            assert isinstance(self.parser_kwargs['parents'], list)
            self.parser_kwargs['parents'].append(get_common_parser())
        else:
            self.parser_kwargs['parents'] = [get_common_parser()]

        if self.view_options:
            self.parser_kwargs['parents'].append(get_view_parser())

        self.name = self.name.lower()

        if 'formatter_class' not in self.parser_kwargs.keys():
            self.parser_kwargs['formatter_class'] = RawTextHelpFormatter

        if 'description' not in self.parser_kwargs.keys():
            self.parser_kwargs['description'] = dedent(getdoc(self))

        if 'epilog' not in self.parser_kwargs.keys():
            self.parser_kwargs['epilog'] = dedent(getdoc(self.run))

        # try to resolve conflicting sub_command names
        if self.name in dict(subparser._get_kwargs())['choices'].keys():
            if self.__module__.split('.')[0] == 'user_commands':
                self.name = 'user_{}'.format(self.name)
            else:
                prefix = self.__module__.split('.')[0].replace('nbcli_', '')
                self.name = '{}_{}'.format(prefix, self.name)

        self.parser = subparser.add_parser(self.name, **self.parser_kwargs)
        self.parser.set_defaults(func=self._pre_run_)
        self.setup()

    def _pre_run_(self, args):

        self.args = args
        self.logger = logging.getLogger('nbcli.'+self.name)
        self._set_log_level_()
        try:
            self.netbox = get_session()
            if self.view_options:
                nbopts = dict(view=self.args.view,
                              view_model=self.args.view_model,
                              cols=self.args.cols,
                              disable_header=self.args.nh)

                self.nbprint = functools.partial(nbprint, **nbopts)
            self.logger.debug(args)

            self.run()
        except Exception as e:
            from traceback import print_tb
            self.logger.critical('%s: %s', type(e).__name__, str(e))

            if self.logger.parent.level <= 10:
                print_tb(e.__traceback__)
            if self.logger.parent.level == 1:
                try:
                    from ipdb import post_mortem
                except:
                    from pdb import post_mortem
                print("\n*** Entering debuger! " + \
                      "(type '?' for help, or 'q' to quit) ***\n")
                post_mortem()

            sys.exit(1)
        except KeyboardInterrupt:
            self.logger.warning('Interrupted by user.')
            sys.exit(0)

    def _set_log_level_(self):
        """Set the loglevel based on the arguments passed."""
        level = self.default_loglevel

        if self.args.quiet:
            level = level + (10 * self.args.quiet)
            if level > 100:
                level = 100

        if self.args.verbose:
            level = level - (10 * self.args.verbose)
            if level < 1:
                level = 1

        self.logger.parent.setLevel(level)

    def setup(self):
        """Define additional parser options for sub command."""
        pass

    def run(self):
        """Execute subcommand."""
        pass
