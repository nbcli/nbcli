from nbcli.views.tools import BaseView

class DcimSitesView(BaseView):

    def table_view(self):

        self.add_col('ID', self.get_attr('id'))
        self.add_col('Name', self.get_attr('name'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Facility', self.get_attr('facility'))
        self.add_col('Region', self.get_attr('region'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('ASN', self.get_attr('asn'))
        self.add_col('Description', self.get_attr('description'))
