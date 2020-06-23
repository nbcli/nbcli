"""Display Views to use for nbcli and nbcmd"""
from collections import OrderedDict
from pynetbox.core.response import Record

class BaseView():

    def __init__(self, obj):

        assert isinstance(obj, Record)
        self.view = OrderedDict()
        self.table_view(obj)

    def __iter__(self):
        return iter(self.view)

    def table_view(self, obj):
        pass

    def detail_view(self, obj):
        pass

    def items(self):
        return self.view.items()

    def keys(self):
        return self.view.keys()

    def values(self):
        return self.view.values()

    def __repr__(self):
        return 'View' + repr(list(self.items()))
