import json
from collections import OrderedDict
from pynetbox.core.response import Record
from ..core.utils import app_model_loc, record_list_check


class BaseView():

    def __init__(self, obj, cols=list()):

        assert isinstance(obj, Record)
        self._obj = obj
        self._view = OrderedDict()
        if cols and isinstance(cols, list) and (len(cols) > 0):
            for col in cols:
                if isinstance(col, str):
                    col = (col, col)
                assert isinstance(col, tuple) and (len(col) == 2)
                self.add_col(col[0], self.get_attr(col[1]))
        else:
            self.table_view()

    @property
    def obj(self):
        return self._obj

    @property
    def view(self):
        return self._view

    def add_col(self, header, value):
        
        if str(value).lower() in ['none', '']:
            value = '-'

        self._view[str(header)] = str(value)

    def get_attr(self, attribute):
        assert isinstance(attribute, str)

        obj = self.obj

        for attr in attribute.lower().split('.'):
            if hasattr(obj, attr):
                obj = getattr(obj, attr)
            else:
                return None

        return obj

    def table_view(self):
        self.add_col('ID', self.get_attr('id'))
        self.add_col(get_view_name(self.obj).replace('View', ''),
                     str(self.obj))

    def detail_view(self):
        lines = list()
        for attr in dict(self.obj).keys():
            lines.append(attr + ': ' + str(self.get_attr(attr)))
        return '\n'.join(lines)

    def items(self):
        return self.view.items()

    def keys(self):
        return self.view.keys()

    def values(self):
        return self.view.values()

    def __iter__(self):
        return iter(self.view)

    def __repr__(self):
        return 'View' + repr(list(self.items()))


def get_json(result):

    def build(data):
        if isinstance(data, Record):
            data = dict(data)
        elif isinstance(data, list):
            data = [build(d) for d in data]
        return data

    data = build(result)

    return json.dumps(data)


def get_view_name(obj):

    assert isinstance(obj, Record)

    class_name = obj.__class__.__name__
    model_loc = app_model_loc(obj)

    if class_name != 'Record':
        return model_loc.split('.')[0].title() + class_name + 'View'

    return model_loc.title().replace('_', '').replace('.', '') + 'View'


def get_view(obj, cols=list()):
    
    for view in BaseView.__subclasses__():
        if view.__name__ == get_view_name(obj):
            return view(obj, cols=cols)

    return BaseView(obj, cols=cols)


def build_table(result, cols=list()):

    display = list()

    if isinstance(result, Record):
        view = get_view(result, cols=cols)
        display.append([str(i) for i in view.keys()])
        display.append([str(i) for i in view.values()])

    if isinstance(result, list):
        assert len(result) > 0
        assert isinstance(result[0], Record)
        assert len(set(entry.__class__ for entry in result)) == 1
        display.append([i for i in get_view(result[0], cols=cols).keys()])
        for entry in result:
            view = get_view(entry, cols=cols)
            display.append([i for i in view.values()])

    return display


def get_table(result, disable_header=False, cols=list()):

    display = build_table(result, cols=cols)
    assert len(display) > 1
    if disable_header:
        display.pop(0)

    # get max width for each column
    colw = list()
    for col in range(len(display[0])):
        colw.append(max([len(row[col]) for row in display]))

    # build template based on max with for each column
    template = ''
    buff = 2
    for w in colw:
        template += '{:<' + str(w + buff) + 's}'

    return '\n'.join([template.format(*entry) for entry in display])


def get_detail(result):

    display = list()

    if isinstance(result, Record):
        view = get_view(result)
        display.append(view.detail_view())

    if isinstance(result, list):
        assert len(result) > 0
        assert isinstance(result[0], Record)
        assert len(set(entry.__class__ for entry in result)) == 1
        for entry in result:
            view = get_view(entry)
            display.append(view.detail_view())

    return ('\n\n' + ('#' * 80) + '\n\n').join(display)

def nbprint(result, view='table', disable_header=False, cols=list()):

    if view == 'json':
        print(get_json(result))
        return

    if isinstance(result, Record):
        result = [result]

    if isinstance(result, list) and record_list_check(result):
        if view == 'detail':
            print(get_detail(result))
        else:
            print(get_table(result, disable_header=disable_header, cols=cols))
    else:
        print(result)
