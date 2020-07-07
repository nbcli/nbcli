"""Display Views to use for nbcli and nbcmd"""
from collections import OrderedDict
from pynetbox.core.response import Record
from ..core.utils import app_model_loc

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
        self.add_col(app_model_loc(self.obj), str(self.obj))

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
