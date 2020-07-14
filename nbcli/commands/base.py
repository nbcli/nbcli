import argparse
import functools
import logging
import sys
from pydoc import getdoc
from textwrap import dedent
from nbcli.core.config import get_session
from nbcli.views.tools import nbprint


def get_common_parser():

    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument('-v', '--verbose',
                        	   action='count',
                        	   help='Show more logging messages')
    common_parser.add_argument('-q', '--quiet',
                        	   action='count',
                       		   help='Show fewer logging messages')
    return common_parser


def get_view_parser():

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


class ProcKWArgsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        setattr(namespace, self.dest, list())
        kw_dest = self.dest + '_kwargs'
        setattr(namespace, kw_dest, dict())
        for i in values:
            if i.find('=') > 0:
                kwargs = getattr(namespace, kw_dest)
                key = i.split('=')[0]
                value = i.split('=')[1]
                if key in kwargs:
                    if isinstance(kwargs[key], list):
                        kwargs[key].append(value)
                    else:
                        kwargs[key] = [kwargs[key], value]
                else:
                    kwargs[key] = value
            else:
                getattr(namespace, self.dest).append(i)


class BaseSubCommand():

    name = 'base'
    parser_kwargs = dict(help='')
    view_options = False

    def __init__(self, subparser):

        if 'parents' in self.parser_kwargs.keys():
            assert isinstance(self.parser_kwargs['parents'], list)
            self.parser_kwargs['parents'].append(get_common_parser())
        else:
            self.parser_kwargs['parents'] = [get_common_parser()]

        if self.view_options:
            self.parser_kwargs['parents'].append(get_view_parser())

        self.name = self.name.lower()

        if 'formatter_class' not in self.parser_kwargs.keys():
            self.parser_kwargs['formatter_class'] = argparse.RawTextHelpFormatter

        if 'description' not in self.parser_kwargs.keys():
            self.parser_kwargs['description'] = dedent(getdoc(self))

        if 'epilog' not in self.parser_kwargs.keys():
            self.parser_kwargs['epilog'] = dedent(getdoc(self.run))

        # try to resolve conflicting sub_command names
        if self.name in dict(subparser._get_kwargs())['choices'].keys():
            if self.__module__.split('.')[0] == 'user_commands':
                self.name = 'user_{}'.format(self.name)
            else:
                prfix = self.__module__.split('.')[0].replace('nbcli_', '')
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
                self.nbprint = functools.partial(nbprint,
                                                 view=self.args.view,
                                                 view_model=self.args.view_model,
                                                 cols=self.args.cols,
                                                 disable_header=self.args.nh)
            self.logger.debug(args)

            self.run()
        except Exception as e:
            self.logger.critical('%s: %s', type(e).__name__, str(e))

            if 0 < self.logger.parent.level <= 10:
                raise e

            sys.exit(1)

    def _set_log_level_(self):
        """Set the loglevel based on the arguments passed."""
        if self.args.quiet:
            if self.args.quiet == 1:
                self.logger.parent.setLevel(logging.ERROR)
            elif self.args.quiet == 2:
                self.logger.parent.setLevel(logging.CRITICAL)
            elif self.args.quiet > 2:
                self.logger.parent.setLevel(100)
        if self.args.verbose:
            if self.args.verbose == 1:
                self.logger.parent.setLevel(logging.INFO)
            elif self.args.verbose > 1:
                self.logger.parent.setLevel(logging.DEBUG)

    def setup(self):
        pass

    def run(self):
        pass
