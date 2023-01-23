from nbcli.views.tools import BaseView


class IpamAggregatesView(BaseView):

    def table_view(self):

        self.add_col('Aggregate', self.get_attr('display'))
        self.add_col('RIR', self.get_attr('rir'))
        self.add_col('Added', self.get_attr('date_added'))
        self.add_col('Description', self.get_attr('description'))


class IpamPrefixesView(BaseView):

    def table_view(self):

        self.add_col('Prefix', self.get_attr('prefix'))
        self.add_col('VLAN', self.get_attr('vlan'))
        self.add_col('VLAN ID', self.get_attr('vlan.vid'))
        self.add_col('Description', self.get_attr('description'))


class IpamIpAddressesView(BaseView):

    def table_view(self):

        self.add_col('IP Address', self.get_attr('address'))
        self.add_col('Vrf', self.get_attr('vrf'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Role', self.get_attr('role'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('Parent', self.get_attr('interface.device'))
        self.add_col('Interface', self.get_attr('interface'))
        self.add_col('DNS Name', self.get_attr('dns_name'))
        self.add_col('Description', self.get_attr('description'))

class IpamVlansView(BaseView):

    def table_view(self):
        self.add_col('VID', self.get_attr('vid'))
        self.add_col('Name', self.get_attr('name'))
        self.add_col('Group', self.get_attr('group'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Role', self.get_attr('role'))
        self.add_col('Description', self.get_attr('description'))
