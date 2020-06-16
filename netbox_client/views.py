"""Display Views to use for nbcli and nbcmd"""

from collections import OrderedDict
from pynetbox.core.response import Record
from .core import app_endpoint_names

def get_view_name(obj):

    if hasattr(obj, 'endpoint'):
        return '-'.join(app_endpoint_names(obj)).title().replace('-', '')

    return ''


def get_view(obj):
    
    for view in BaseView.__subclasses__():
        if view.__name__ == get_view_name(obj):
            return view(obj)

    return RecordView(obj)


def build_display_matrix(result):

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


def display_result(result, header=True):

    display = build_display_matrix(result)
    assert len(display) > 1
    if not header:
        display.pop(0)

    template = '{:<15s}' * len(display[0])
    for entry in display:
        print(template.format(*entry))

class BaseView():

    def __init__(self, obj):

        assert isinstance(obj, Record)
        self.view = OrderedDict()
        self.view_model(obj)

    def __iter__(self):
        return iter(self.view)

    def view_model(self, obj):
        pass

    def items(self):
        return self.view.items()

    def keys(self):
        return self.view.keys()

    def values(self):
        return self.view.values()

    def __repr__(self):
        return 'View' + repr(list(self.items()))


class RecordView(BaseView):

    def view_model(self, obj):

        idkey = obj.endpoint.name.title().replace('-', '') + 'ID'

        self.view[idkey] = obj.id
        self.view['Name'] = str(obj)


class DcimDevices(BaseView):

    def view_model(self, obj):

        self.view['DeviceID'] = obj.id
        self.view['Name'] = obj.name
        self.view['Model'] = obj.device_type.model
        self.view['SN'] = obj.serial
        self.view['Rack'] = obj.rack
        self.view['Position'] = obj.position


class DcimInterfaces(BaseView):

    def view_model(self, obj):

        endpoint = ''
        if obj.connected_endpoint:
            endpoint = str(obj.connected_endpoint.device) + '['
            endpoint += str(obj.connected_endpoint) + ']'

        cable = ''
        if obj.cable:
            cable = '<-' + str(obj.cable.id) + '->'

        self.view['InterfaceID'] = obj.id
        self.view['Name'] = str(obj.device) + '[' + str(obj.name) + ']'
        self.view['Cable'] = cable
        self.view['ConnectedEndpoint'] = endpoint
