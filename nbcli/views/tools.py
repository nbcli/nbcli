import json
from pynetbox.core.response import Record
from .base import BaseView
from .record import RecordView
from ..core import endpoint_loc

def get_json(result):

    def build(data):
        if isinstance(data, Record):
            data = dict(data)
        elif isinstance(data, list):
            data = [build(d) for d in data]
        return data

    data = build(result)

    return json.dumps(data, indent=4)


def get_view_name(obj):

    if hasattr(obj, 'endpoint'):
        ep_loc = endpoint_loc(obj)
        return ep_loc.title().replace('_', '').replace('.', '') + 'View'

    return ''


def get_view(obj):
    
    for view in BaseView.__subclasses__():
        if view.__name__ == get_view_name(obj):
            return view(obj)

    return RecordView(obj)


def build_table(result):

    display = list()

    if isinstance(result, Record):
        view = get_view(result)
        display.append([str(i) for i in view.keys()])
        display.append([str(i) for i in view.values()])

    if isinstance(result, list):
        assert len(result) > 0
        assert isinstance(result[0], Record)
        assert len(set(entry.__class__ for entry in result)) == 1
        display.append([str(i) for i in get_view(result[0]).keys()])
        for entry in result:
            view = get_view(entry)
            display.append([str(i) for i in view.values()])

    return display


def get_table(result, disable_header=False):

    display = build_table(result)
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


def nbprint(result, view='table', disable_header=False, cols=list()):

    assert result

    if view == 'detail':
        print(get_json(result))
    elif view == 'json':
        print(get_json(result))
    else:
        print(get_table(result, disable_header=disable_header))
