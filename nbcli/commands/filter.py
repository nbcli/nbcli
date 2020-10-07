from pynetbox.core.response import Record
from nbcli.commands.base import BaseSubCommand
from nbcli.commands.tools import NbArgs
from nbcli.core.utils import app_model_by_loc, is_list_of_records


class Filter():

    def __init__(self,
                 netbox,
                 model,
                 args=list(),
                 get=False,
                 count=False,
                 delete=False,
                 ud=list(),
                 de=list()):

        self.model = app_model_by_loc(netbox, model)

        method = 'all'

        if get:
            method = 'get'
        elif count:
            method = 'count'
        elif args:
            method = 'filter'

        self.method = getattr(self.model, method)

        nba = NbArgs(netbox)
        nba.proc(*args)
        result = self.method(*nba.args, **nba.kwargs)

        if isinstance(result, Record):
            result = [result]

        if is_list_of_records(result):
            if delete:
                self.delete(result)
            elif ud:
                ud_nba = NbArgs(netbox)
                ud_nba.proc(*ud)
                self.update(result, **ud_nba.kwargs)
            elif de:
                detail = de.pop(0)
                de_nba = NbArgs(netbox)
                de_nba.proc(*de)
                self.detail(result, detail, *de_nba.args, **de_nba.kwargs)
            else:
                self.result = result
        else:
            self.result = result

    def delete(self, result):
        assert is_list_of_records(result)
        anslist = list()
        for obj in result:
            anslist.append('{} ({})'.format(str(obj), str(obj.id)))
        ans = input('Delete {}?\n* {}\n(yes) to delete: '. \
                    format(obj.__class__.__name__,
                           '\n* '.join(anslist)))
        if ans.lower() == 'yes':
            dellist = list()
            for obj in result:
                objrep = '{} ({})'.format(str(obj), str(obj.id))
                if obj.delete():
                    dellist.append('{} Deleted!'.format(objrep))
                else:
                    dellist.append('Error deleting {}'.format(objrep))
            result = '\n'.join(dellist)
        else:
            self.result = 'Aborting!'

    def update(self, result, **kwargs):
        assert is_list_of_records(result)
        anslist = list()
        for obj in result:
            anslist.append('{} ({})'.format(str(obj), str(obj.id)))
        ans = input('Update {} with {}?\n* {}\n(yes) to update: '. \
                    format(obj.__class__.__name__,
                           str(kwargs),
                           '\n* '.join(anslist)))
        if ans.lower() == 'yes':
            udlist = list()
            for obj in result:
                objrep = '{} ({})'.format(str(obj), str(obj.id))
                if obj.update(kwargs):
                    udlist.append('{} Updated!'.format(objrep))
                else:
                    udlist.append('Error updating {}'.format(objrep))
            result = '\n'.join(udlist)
        else:
            self.result = 'Aborting!'

        self.result = obj.update(kwargs)

    def detail(self, result, detail, *args, **kwargs):
        assert is_list_of_records(result)
        self.result = list()
        for obj in result:
            de = getattr(obj, detail)
            self.result += de.list(*args, **kwargs)


class FilterSubCommand(BaseSubCommand):

    name = 'filter'
    parser_kwargs = dict(help='Filter NetBox objects.')
    view_options = True


    def setup(self):
    
        self.parser.add_argument('model',
                            help="NetBox model")
    
        self.parser.add_argument('args',
                            nargs='*',
                            help='Argumnet(s) to filter results.')

        self.parser.add_argument('-g', '--get',
                                 action='store_true',
                                 help='Get single result. '+ \
                                      'Raise error if more are returned')
    
        obj_meth = self.parser.add_mutually_exclusive_group()
    
        obj_meth.add_argument('-c', '--count',
                              action='store_true',
                              help='Return the count of objects in filter.')

        obj_meth.add_argument('-D', '--delete',
                              action='store_true',
                              help='Delete Object(s) retrieved by get method')
    
        obj_meth.add_argument('--ud', '--update',
                              nargs='*',
                              help='Update object(s) with given kwargs')
    
        self.parser.add_argument('--de', '--detail-endpoint',
                            nargs='*',
                            help='List results from detail endpoint '+ \
                                 'With optional kwargs')


    def run(self):
    
        nbfilter = Filter(self.netbox,
                          self.args.model,
                          args=self.args.args or [],
                          get=self.args.get,
                          count=self.args.count,
                          delete=self.args.delete,
                          ud=self.args.ud or [],
                          de=self.args.de or [])

        if nbfilter.result:
            self.nbprint(nbfilter.result, cols=self.args.cols)
        else:
            self.logger.warning('No results found')
