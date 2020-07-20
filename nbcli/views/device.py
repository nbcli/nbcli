from nbcli.views.tools import BaseView, Formatter

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

    def detail_view(self):

        lines = list()
        lines.append('{}\n{}'.format(self.obj, '=' * len(str(self.obj))))

        lines.append('\nDevice\n------')
        lines.append('{}:\t{}'.format('Site', self.get_attr('site')))
        lines.append('{}:\t{}'.format('Rack', self.get_attr('rack')))
        lines.append('{}:\t{}'.format('Position', self.get_attr('position')))
        lines.append('{}:\t{}'.format('Tenant', self.get_attr('tenant')))
        lines.append('{}:\t{}'.format('Device Type', self.get_attr('device_type')))
        lines.append('{}:\t{}'.format('Serial Number', self.get_attr('serial')))
        lines.append('{}:\t{}'.format('Asset Tag', self.get_attr('asset_tag')))

        lines.append('\nManagement\n----------')
        lines.append('{}:\t{}'.format('Role', self.get_attr('role')))
        lines.append('{}:\t{}'.format('Platform', self.get_attr('platform')))
        lines.append('{}:\t{}'.format('Status', self.get_attr('status')))
        lines.append('{}:\t{}'.format('Primary IPv4', self.get_attr('primary_ip4')))
        lines.append('{}:\t{}'.format('Primary IPv6', self.get_attr('primary_ip6')))
        
        lines.append('\nCustom Fields\n-------------')
        for key, value in self.obj.custom_fields.items():
            lines.append('{}:\t{}'.format(key, value))

        lines.append('\nTags\n----')
        lines.append(' '.join(self.obj.tags))

        lines.append('\nComments\n--------')
        lines.append(self.get_attr('comments'))

        ifaces = self.obj.api.dcim.interfaces.filter(device_id=self.obj.id)
        cols = [('Name', 'name'),
                 ('LAG', 'lag'),
                 ('Description', 'description'),
                 ('MTU', 'mtu'),
                 ('Mode', 'mode'),
                 ('Cable', 'cable.id'),
                 ('Connection', 'connected_endpoint.device'),
                 ('', 'connected_endpoint')]
        if len(ifaces) > 0:
            lines.append('\nInterfaces\n----------')
            lines.append(Formatter(ifaces, cols=cols).string)
        

        return '\n'.join(lines)
