import argparse
import sys
from pprint import pprint
from .core import get_session, is_record, add_detail_endpoint

ENDPOINT_METHODS =  ('all', 'choices', 'count', 'create', 'filter', 'get')

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


class CLI():

    def __init__(self,
                 app,
                 endpoint,
                 method,
                 args=list(),
                 kwargs=dict(),
                 delete=False,
                 update=list(),
                 update_kwargs=dict(),
                 de=list(),
                 dea=list(),
                 dea_kwargs=dict()):

        assert method in ENDPOINT_METHODS, \
            'Allowed methods ' + str(ENDPOINT_METHODS)

        self.netbox = get_session()
        self.app = getattr(self.netbox, app)
        self.endpoint = getattr(self.app, endpoint)
        self.method = getattr(self.endpoint, method)
        self.result = self.method(*args, **kwargs)

    def display(self):

        if not self.result:
            print('No result to display')
        elif isinstance(self.result, int):
            print(self.result)
        elif isinstance(self.result, list):
            for i in self.result:
                if is_record(i):
                    print('({}) {}'.format(i.id, i))
                else:
                    print(i)
        elif is_record(self.result):
            pprint(dict(self.result))
        else:
            print(self.result)

    def delete(self, obj):
        print('Not Implemented!')

    def update(self, obj):
        print('Not Implemented!')

    def detail(self, obj):
        print('Not Implemented!')

def main():

    parser = argparse.ArgumentParser(description='nbcli', prog='nbcli')

    parser.add_argument('app',
                        metavar="APP",
                        type=str,
                        help="App to call")

    parser.add_argument('endpoint',
                        metavar="ENDPOINT",
                        type=str,
                        help="App endpoint")

    parser.add_argument('method',
                        metavar="METHOD",
                        type=str,
                        choices=ENDPOINT_METHODS,
                        help="Endpoint Method")

    parser.add_argument('args',
                        nargs='*',
                        action=ProcKWArgsAction,
                        help='Argumnet to pass to func')

    obj_meth = parser.add_mutually_exclusive_group()

    obj_meth.add_argument('-D', '--delete',
                          action='store_true',
                          help='Delete Object retrieved by get method')

    obj_meth.add_argument('-u', '--update',
                          metavar='UD-ARGS',
                          nargs='+',
                          action=ProcKWArgsAction,
                          help='Update object with given kwargs')

    obj_meth.add_argument('--de', '--detail-endpoint',
                          metavar=('DE', 'DE-METHOD'),
                          nargs=2,
                          help='Get the detail endpoint of object')

    parser.add_argument('--dea', '--de-args',
                        metavar='DE-ARGS',
                        nargs='*',
                        action=ProcKWArgsAction,
                        help='Argumets to pass to the de-action')

    args = parser.parse_args()

    if args.update is None:
        args.update = list()
        args.update_kwargs = dict()

    if args.de is None:
        args.de = list()

    if args.dea is None:
        args.dea = list()
        args.dea_kwargs = dict()

    print(args)

    try:
        cli = CLI(args.app,
                  args.endpoint,
                  args.method,
                  args=args.args,
                  kwargs=args.args_kwargs,
                  delete=args.delete,
                  update=args.update,
                  update_kwargs=args.update_kwargs,
                  de=args.de,
                  dea=args.dea,
                  dea_kwargs=args.dea_kwargs)

        cli.display()
    except Exception as e:
        print(type(e).__name__)
        print(e)
        #from IPython import embed; embed()

        sys.exit(1)

if __name__ == '__main__':
    main()
