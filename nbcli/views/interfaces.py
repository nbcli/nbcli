from nbcli.views.tools import BaseView

class DcimInterfacesView(BaseView):

    def table_view(self):

        self.add_col('ID', self.get_attr('id'))
        self.add_col('Parent', self.get_attr('device'))
        self.add_col('Name', self.get_attr('name'))
        self.add_col('Enabled', self.get_attr('enabled'))
        self.add_col('Type', self.get_attr('type'))
        self.add_col('Description', self.get_attr('description'))
        self.add_col('cable', self.get_attr('cable.id'))
