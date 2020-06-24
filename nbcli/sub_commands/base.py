import argparse
import logging
from ..core import get_session

view_parser = argparse.ArgumentParser(add_help=False)
view_parser.add_argument('--view', type=str, help='Output view.',
                           choices=['table', 'detail', 'json'],
                           default='table')
view_parser.add_argument('--cols', nargs='*',
                           help="Custome columns for table output.")
view_parser.add_argument('--nh', '--no-header',
                         action='store_false',
                         help='Disable header row in results')


class ProcKWArgsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        setattr(namespace, self.dest, list())
        kw_dest = self.dest + '_kwargs'
        setattr(namespace, kw_dest, dict())
        for i in values:
            if i.find('=') > 0:
                getattr(namespace, kw_dest)[i.split('=')[0]] = i.split('=')[1]
            else:
                getattr(namespace, self.dest).append(i)


class BaseSubCommand():

    name = 'base'
    parser_kwargs = dict()

    def __init__(self, subparser, parents=list()):

        if 'parents' in self.parser_kwargs.keys():
            assert isinstance(self.parser_kwargs['parents'], list)
            self.parser_kwargs['parents'] += parents
        else:
            self.parser_kwargs['parents'] = parents

        self.name = self.name.lower()
        self.parser = subparser.add_parser(self.name, **self.parser_kwargs)
        self.parser.set_defaults(func=self._pre_run_)
        self.setup()

    def _pre_run_(self, args):
        
        self.args = args
        self.netbox = get_session(conf_file=args.config)
        self.logger = logging.getLogger('nbcli.'+self.name)
        self.run()


    def setup(self):
        pass

    def run(self):
        pass
