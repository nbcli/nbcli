"""Define Classes and Functions for use by views."""

import json
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from pynetbox.core.response import Record, RecordSet
from nbcli.core.utils import is_list_of_records, view_name, rend_table


class BaseView:
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
        if str(value).lower() in ["none", ""]:
            value = "-"

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

        for attr in attribute.split("."):
            keys = attr.split(":")[1:]
            attr = attr.split(":")[0]

            if hasattr(obj, attr.lower()):
                obj = getattr(obj, attr.lower())
                for key in keys:
                    obj = get_val(obj, key)
            else:
                return None

        return obj

    def table_view(self):
        """Define headers and values for table view of object."""
        self.add_col("ID", self.get_attr("id"))
        self.add_col(view_name(self.obj).replace("View", ""), str(self.obj))

    def detail_view(self):
        """Define detail view of object."""
        lines = list()
        for attr in dict(self.obj).keys():
            lines.append(attr + ": " + str(self.get_attr(attr)))
        return "\n".join(lines)

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
        return "View" + repr(list(self.items()))


class Formatter:
    """Format result from pynetbox based on given peramiters."""

    def __init__(
        self,
        result,
        json_view=False,
        detail_view=False,
        view_model=None,
        cols=list(),
        disable_header=False,
    ):
        """Initialize Display instance."""
        if isinstance(result, RecordSet):
            result = list(result)
        self.result = result
        self.json_view = json_view
        self.detail_view = detail_view
        self.view_model = view_model
        self.cols = cols
        self.disable_header = disable_header
        self._string = ""
        self._threading = False
        self._max_workers = 4

    def _build_table(self):
        display = list()

        # add table header
        hview = self.view_model(self.result[0], cols=self.cols)
        display.append([k for k in hview.keys()])

        def thread_worker(entry):
            view = self.view_model(entry, cols=self.cols)
            return [v for v in view.values()]

        if self._threading:
            with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
                results = executor.map(thread_worker, self.result)
            display = display + list(results)
        else:
            for entry in self.result:
                view = self.view_model(entry, cols=self.cols)
                display.append([v for v in view.values()])

        return display

    def _get_detail(self):
        display = list()

        for entry in self.result:
            display.append(self.view_model(entry).detail_view())

        self._string = ("\n\n" + ("#" * 80) + "\n\n").join(display)

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

        self._string = rend_table(display)

    def _get_view(self):
        # probably not the best way to do this, but first opportunity
        # to get threading and max_workers from conf
        nb = self.result[0].api
        self._threading = nb.threading
        self._max_workers = nb.nbcli.conf.nbcli.get("max_workers", 4)

        if not self.view_model:
            self.view_model = view_name(self.result[0])

        if isinstance(self.view_model, str):
            if self.view_model == "BaseView":
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
        """Generate string based on parameters passed to Display."""
        if self.json_view:
            self._get_json()
            return self._string

        if isinstance(self.result, Record):
            self.result = [self.result]

        if isinstance(self.result, list) and is_list_of_records(self.result):
            self._get_view()
            if self.detail_view:
                self._get_detail()
            else:
                self._get_table()
        else:
            self._string = str(self.result)

        return self._string


def nbprint(
    result,
    json_view=False,
    detail_view=False,
    view_model=None,
    cols=list(),
    disable_header=False,
    string=False,
):
    """Print result from pynetbox."""
    formatted_result = Formatter(
        result,
        json_view=json_view,
        detail_view=detail_view,
        view_model=view_model,
        cols=cols,
        disable_header=disable_header,
    )
    if string:
        return formatted_result.string
    else:
        print(formatted_result.string)
