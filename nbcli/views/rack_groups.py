from nbcli.views.tools import BaseView

class DcimRackGroupsView(BaseView):

    def table_view(self):

        self.add_col('ID', self.get_attr('id'))
        self.add_col('Name', self.get_attr('name'))
        self.add_col('Site', self.get_attr('site'))
        self.add_col('Racks', self.get_attr('rack_count'))
        self.add_col('Description', self.get_attr('description'))
