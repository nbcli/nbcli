from nbcli.views.tools import BaseView

class DcimRacksView(BaseView):

    def table_view(self):

        self.add_col('Name', self.get_attr('name'))
        self.add_col('Site', self.get_attr('site'))
        self.add_col('Group', self.get_attr('group'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Facility ID', self.get_attr('facility_id'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('Role', self.get_attr('role'))
        self.add_col('Height', self.get_attr('u_height'))
        self.add_col('Devices', self.get_attr('device_count'))


class DcimRUsView(BaseView):

    def table_view(self):

        self.add_col('Name', self.get_attr('name'))
        self.add_col('Device', self.get_attr('device'))
        self.add_col('Role', self.get_attr('device.device_role'))
        self.add_col('Type', self.get_attr('device.device_type'))
        self.add_col('Serial', self.get_attr('device.serial'))
