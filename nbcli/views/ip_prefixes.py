from nbcli.views.tools import BaseView

class IpamPrefixesView(BaseView):

    def table_view(self):

        self.add_col('Prefix', self.get_attr('prefix'))
        self.add_col('VLAN', self.get_attr('vlan'))
        self.add_col('VLAN ID', self.get_attr('vlan.vid'))
        self.add_col('Description', self.get_attr('description'))
