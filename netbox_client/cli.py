import argparse
import sys
from pprint import pprint
from .core import Config, get_session

class ProcArgsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        setattr(namespace, 'kwargs', dict())
        setattr(namespace, 'args', list())
        for i in values:
            if i.find('=') > 0:
                namespace.kwargs[i.split('=')[0]] = i.split('=')[1]
            else:
                namespace.args.append(i)


class CLI():

    def __init__(self, app, endpoint, func, args=list(), kwargs=dict()):

        allowed_func = ['all', 'choices', 'count', 'create', 'filter', 'get']
        assert func in allowed_func, 'Allowed func ' + str(allowed_func)

        self.netbox = get_session()
        self.app = getattr(self.netbox, app)
        self.endpoint = getattr(self.app, endpoint)
        self.func = getattr(self.endpoint, func)
        self.result = self.func(*args, **kwargs)

    def display(self):

        if not self.result:
            print('No result to display')
        elif isinstance(self.result, int):
            print(self.result)
        elif isinstance(self.result, list):
            for i in self.result:
                print('({}) {}'.format(i.id, i))
        else:
            pprint(dict(self.result))


def main():

    parser = argparse.ArgumentParser(description='nbcli', prog='nbcli')
    parser.add_argument('app', type=str, help="App to call")
    parser.add_argument('endpoint', type=str, help="App endpoint")
    parser.add_argument('func', type=str, help="Endpoint Function")
    parser.add_argument('args', nargs='*', action=ProcArgsAction, help='Argumnet to pass to func')
    args = parser.parse_args()

    try:
        cli = CLI(args.app, args.endpoint, args.func, args=args.args, kwargs=args.kwargs)
        cli.display()
    except Exception as e:
        print(type(e).__name__)
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    main()
