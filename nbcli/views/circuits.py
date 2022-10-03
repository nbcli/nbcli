from nbcli.views.tools import BaseView

class CircuitsProvidersView(BaseView):


    def table_view(self):


        self.add_col('Name', self.get_attr('name'))
        self.add_col('ASN', self.get_attr('asn'))
        self.add_col('Account Number', self.get_attr('account'))
        self.add_col('Circuits', self.get_attr('circuit_count'))


class CircuitsCircuitTypesView(BaseView):


    def table_view(self):


        self.add_col('Name', self.get_attr('name'))
        self.add_col('Circuits', self.get_attr('circuit_count'))
        self.add_col('Slug', self.get_attr('slug'))
        self.add_col('Description', self.get_attr('description'))


class CircuitsCircuitsView(BaseView):


    def table_view(self):


        self.add_col('ID', self.get_attr('cid'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Type', self.get_attr('type'))
        self.add_col('Provider', self.get_attr('provider'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('A Side', self.get_attr('termination_a'))
        self.add_col('Z Side', self.get_attr('termination_z'))
        self.add_col('Description', self.get_attr('description'))
