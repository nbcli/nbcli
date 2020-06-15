"""Display Views to use for nbcli and nbcmd"""

from collections import OrderedDict
from pynetbox.core.response import Record
from .core import app_endpoint_names

class RecordView():

    def __init__(self, obj):

        assert isinstance(obj, Record)
        self.obj = obj
        self.view = OrderedDict()
        self.view_model()

    def __iter__(self):
        return self.view.__iter__()

    def view_model(self):

        idkey = self.obj.endpoint.name.title().replace('-', '') + 'ID'

        self.view[idkey] = self.obj.id
        self.view['Name'] = str(self.obj)

    def items(self):
        return self.view.items()

    def keys(self):
        return self.view.keys()

    def values(self):
        return self.view.values()


class DcimDevices(RecordView):

    def view_model(self):

        self.view['DeviceID'] = self.obj.id
        self.view['Name'] = self.obj.name
        self.view['Model'] = self.device_type.model
        self.view['SN'] = self.obj.serial
        self.view['Rack'] = self.obj.rack
        self.view['Position'] = self.obj.position
