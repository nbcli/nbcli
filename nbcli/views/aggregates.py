from nbcli.views.tools import BaseView

class IpamAggregatesView(BaseView):

    def table_view(self):

        self.add_col('ID', self.get_attr('id'))
        self.add_col('Aggregate', self.get_attr('aggregate'))
        self.add_col('RIR', self.get_attr('rir'))
        self.add_col('Added', self.get_attr('date_added'))
        self.add_col('Description', self.get_attr('description'))
