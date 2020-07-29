"""Define Classes and Functions for use by views."""

import json
from collections import OrderedDict
from pynetbox.core.response import Record
from nbcli.core.utils import app_model_loc, is_list_of_records


class BaseView():
    """Base (default) view used to create other netbox object views."""

    def __init__(self, obj, cols=list()):
        """Populate _view based on defined table_view of passed cols."""
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
        """Return object associated with view instance."""
        return self._obj

    @property
    def view(self):
        """Return populated OrderedDict."""
        return self._view

    def add_col(self, header, value):
        """Convert header/value to string and add to view."""
        if str(value).lower() in ['none', '']:
            value = '-'

        self._view[str(header)] = str(value)

    def get_attr(self, attribute):
        """Resolve attribute of assigned object.

        Return the value, or None if it does not exist.
        """
        assert isinstance(attribute, str)

        def get_val(obj, key):

            if isinstance(obj, dict) and (key in obj):
                return obj[key]
            elif isinstance(obj, list) and key.isdigit() and (len(obj) > int(key)):
                return obj[int(key)]
            else:
                return None

        obj = self.obj

        for attr in attribute.split('.'):

            keys = attr.split(':')[1:]
            attr = attr.split(':')[0]

            if hasattr(obj, attr.lower()):
                obj = getattr(obj, attr.lower())
                for key in keys:
                    obj = get_val(obj, key)
            else:
                return None

        return obj

    def table_view(self):
        """Define headers and values for table view of object."""
        self.add_col('ID', self.get_attr('id'))
        self.add_col(get_view_name(self.obj).replace('View', ''),
                     str(self.obj))

    def detail_view(self):
        """Define detail view of object."""
        lines = list()
        for attr in dict(self.obj).keys():
            lines.append(attr + ': ' + str(self.get_attr(attr)))
        return '\n'.join(lines)

    def items(self):
        """Return items of OrderedDict."""
        return self.view.items()

    def keys(self):
        """Return keys of OrderedDict."""
        return self.view.keys()

    def values(self):
        """Get values of OrderedDict."""
        return self.view.values()

    def __iter__(self):
        """Get iterator of OrderedDict."""
        return iter(self.view)

    def __repr__(self):
        """Meaningful repr."""
        return 'View' + repr(list(self.items()))


def get_view_name(obj):
    """Generate view name based on class, url, or endpoint url."""
    assert isinstance(obj, Record)

    class_name = obj.__class__.__name__
    model_loc = app_model_loc(obj)

    if class_name != 'Record':
        return model_loc.split('.')[0].title() + class_name + 'View'

    return model_loc.title().replace('_', '').replace('.', '') + 'View'


class Formatter():
    """Format result from pynetbox based on given peramiters."""

    def __init__(self,
                 result,
                 view='table',
                 view_model=None,
                 cols=list(),
                 disable_header=False):
        """Initialize Display instance."""
        self.result = result
        self.view = view
        self.view_model = view_model
        self.cols = cols
        self.disable_header = disable_header
        self._string = ''

    def _build_table(self):

        display = list()

        for i, entry in enumerate(self.result):
            view = self.view_model(entry, cols=self.cols)
            if i == 0:
                display.append([i for i in view.keys()])
            display.append([i for i in view.values()])

        return display

    def _get_detail(self):

        display = list()

        for entry in self.result:
            display.append(self.view_model(entry).detail_view())

        self._string = ('\n\n' + ('#' * 80) + '\n\n').join(display)

    def _get_json(self):

        def build(data):
            if isinstance(data, Record):
                data = dict(data)
            elif isinstance(data, list):
                data = [build(d) for d in data]
            return data

        self._string = json.dumps(build(self.result))

    def _get_table(self):

        display = self._build_table()
        assert len(display) > 1
        if self.disable_header:
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

        self._string = '\n'.join([template.format(*row) for row in display])

    def _get_view(self):

        if not self.view_model:
            self.view_model = get_view_name(self.result[0])

        if isinstance(self.view_model, str):

            if self.view_model == 'BaseView':
                self.view_model = BaseView
                return

            view_names = [view.__name__ for view in BaseView.__subclasses__()]

            if self.view_model not in view_names:
                self.view_model = BaseView
                return

            for view in reversed(BaseView.__subclasses__()):
                if view.__name__ == self.view_model:
                    self.view_model = view
                    return

        if isinstance(self.view_model.__class__, BaseView.__class__):
            return

        self.view_model = BaseView

    @property
    def string(self):
        """Generate string based on peramiters passed to Display."""
        if self.view == 'json':
            self._get_json()
            return self._string

        if isinstance(self.result, Record):
            self.result = [self.result]

        if isinstance(self.result, list) and is_list_of_records(self.result):
            self._get_view()
            if self.view == 'detail':
                self._get_detail()
            else:
                self._get_table()
        else:
            self._string = str(self.result)

        return self._string


def nbprint(result,
            view='table',
            view_model=None,
            cols=list(),
            disable_header=False):
    """Print result from pynetbox."""
    formatted_result = Formatter(result,
                                 view=view,
                                 view_model=view_model,
                                 cols=cols,
                                 disable_header=disable_header)

    print(formatted_result.string)
