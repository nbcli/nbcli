from .base import BaseView

class DcimInterfacesView(BaseView):

    def table_view(self, obj):

#        endpoint = ''
#        if obj.connected_endpoint:
#            endpoint = str(obj.connected_endpoint.device) + '['
#            endpoint += str(obj.connected_endpoint) + ']'
#
#        cable = ''
#        if obj.cable:
#            cable = '<-' + str(obj.cable.id) + '->'
#
#        self.view['InterfaceID'] = obj.id
#        self.view['Name'] = str(obj.device) + '[' + str(obj.name) + ']'
#        self.view['Cable'] = cable
#        self.view['ConnectedEndpoint'] = endpoint
        self.view['ID'] = obj.id
        self.view['Parent'] = obj.device
        self.view['Name'] = obj.name
        self.view['Enabled'] = obj.enabled
        self.view['Type'] = obj.type
        self.view['Description'] = obj.description
        if obj.cable:
            self.view['cable'] = obj.cable.id
        else:
            self.view['cable'] = '-'
