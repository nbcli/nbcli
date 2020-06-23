from .base import BaseView

class DcimDevicesView(BaseView):

    def table_view(self, obj):

        self.view['ID'] = obj.id
        self.view['Name'] = obj.name
        self.view['Status'] = obj.status
        self.view['Tenant'] = obj.tenant
        self.view['Site'] = obj.site
        self.view['Rack'] = obj.rack
        self.view['Role'] = obj.device_role
        self.view['Type'] = obj.device_type
        self.view['IP Address'] = str(obj.primary_ip).split('/', 1)[0]
