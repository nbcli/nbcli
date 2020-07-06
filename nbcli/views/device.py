from .base import BaseView

class DcimDevicesView(BaseView):

    def table_view(self):

        self.add_col('ID', self.get_attr('id'))
        self.add_col('Name', self.get_attr('name'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('Site', self.get_attr('site'))
        self.add_col('Rack', self.get_attr('rack'))
        self.add_col('Role', self.get_attr('device_role'))
        self.add_col('Type', self.get_attr('device_type'))
        self.add_col('IP Address', str(self.get_attr('primary_ip')).split('/')[0])
