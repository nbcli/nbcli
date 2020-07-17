from nbcli.views.tools import BaseView

class DcimRacksView(BaseView):

    def table_view(self):

        self.add_col('ID', self.get_attr('id'))
        self.add_col('Name', self.get_attr('name'))
        self.add_col('Site', self.get_attr('site'))
        self.add_col('Group', self.get_attr('group'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Facility ID', self.get_attr('facility_id'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('Role', self.get_attr('role'))
        self.add_col('Height', self.get_attr('u_height'))
        self.add_col('Devices', self.get_attr('device_count'))
