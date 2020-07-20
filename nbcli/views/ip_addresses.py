from nbcli.views.tools import BaseView

class IpamIpAddressesView(BaseView):

    def table_view(self):

        self.add_col('ID', self.get_attr('id'))
        self.add_col('IP Address', self.get_attr('address'))
        self.add_col('Vrf', self.get_attr('vrf'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Role', self.get_attr('role'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('Parent', self.get_attr('interface.device'))
        self.add_col('Interface', self.get_attr('interface'))
        self.add_col('DNS Name', self.get_attr('dns_name'))
        self.add_col('Description', self.get_attr('description'))
