from nbcli.views.tools import BaseView
from nbcli.core.utils import view_name

class ResourceView(BaseView):

    def table_view(self):
        """Define headers and values for table view of object."""
        self.add_col('ID', self.get_attr('id'))
        self.add_col(view_name(self.obj).replace('View', ''),
                     str(self.obj))

    def detail_view(self):
        """Define detail view of object."""
        lines = list()
        for attr in dict(self.obj).keys():
            lines.append(attr + ': ' + str(self.get_attr(attr)))
        return '\n'.join(lines)
