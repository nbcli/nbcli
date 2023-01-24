from nbcli.views.tools import BaseView

#class DcimCableTerminationsView(BaseView):
#class DcimCablesView(BaseView):
#class DcimConnectedDeviceView(BaseView):
#class DcimConsolePortTemplatesView(BaseView):
#class DcimConsolePortsView(BaseView):
#class DcimConsoleServerPortTemplatesView(BaseView):
#class DcimConsoleServerPortsView(BaseView):
#class DcimDeviceBayTemplatesView(BaseView):
#class DcimDeviceBaysView(BaseView):
#class DcimDeviceRolesView(BaseView):


class DcimDeviceTypesView(BaseView):

    def table_view(self):

        self.add_col('Device Type', self.get_attr('model'))
        self.add_col('Manufacturer', self.get_attr('manufacturer'))
        self.add_col('Part Number', self.get_attr('part_number'))
        self.add_col('Height (U)', self.get_attr('u_height'))
        self.add_col('Full Depth', self.get_attr('is_full_depth'))
        self.add_col('Parent/child status', self.get_attr('subdevice_role'))
        self.add_col('Instances', self.get_attr('device_count'))

class DcimDevicesView(BaseView):

    def table_view(self):

        self.add_col('Name', self.get_attr('name'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('Site', self.get_attr('site'))
        self.add_col('Rack', self.get_attr('rack'))
        self.add_col('Role', self.get_attr('device_role'))
        self.add_col('Type', self.get_attr('device_type'))
        self.add_col('IP Address', str(self.get_attr('primary_ip')).split('/')[0])


#class DcimFrontPortTemplatesView(BaseView):
#class DcimFrontPortsView(BaseView):
#class DcimInterfaceTemplatesView(BaseView):


class DcimInterfacesView(BaseView):

    def table_view(self):

        self.add_col('Parent', self.get_attr('device'))
        self.add_col('Name', self.get_attr('name'))
        self.add_col('Enabled', self.get_attr('enabled'))
        self.add_col('Type', self.get_attr('type'))
        self.add_col('Description', self.get_attr('description'))
        self.add_col('cable', self.get_attr('cable.id'))


#class DcimInventoryItemRolesView(BaseView):
#class DcimInventoryItemTemplatesView(BaseView):
#class DcimInventoryItemsView(BaseView):


class DcimLocationsView(BaseView):

    def table_view(self):

        self.add_col('Name', self.get_attr('name'))
        self.add_col('Site', self.get_attr('site'))
        self.add_col('Racks', self.get_attr('rack_count'))
        self.add_col('Description', self.get_attr('description'))


#class DcimManufacturersView(BaseView):
#class DcimModuleBayTemplatesView(BaseView):
#class DcimModuleBaysView(BaseView):
#class DcimModuleTypesView(BaseView):
#class DcimModulesView(BaseView):
#class DcimPlatformsView(BaseView):
#class DcimPowerFeedsView(BaseView):
#class DcimPowerOutletTemplatesView(BaseView):
#class DcimPowerOutletsView(BaseView):
#class DcimPowerPanelsView(BaseView):
#class DcimPowerPortTemplatesView(BaseView):
#class DcimPowerPortsView(BaseView):
#class DcimRackReservationsView(BaseView):
#class DcimRackRolesView(BaseView):
#class DcimRacksView(BaseView):


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


#class DcimRearPortTemplatesView(BaseView):
#class DcimRearPortsView(BaseView):
#class DcimRegionsView(BaseView):
#class DcimSiteGroupsView(BaseView):


class DcimSitesView(BaseView):

    def table_view(self):

        self.add_col('Name', self.get_attr('name'))
        self.add_col('Status', self.get_attr('status'))
        self.add_col('Facility', self.get_attr('facility'))
        self.add_col('Region', self.get_attr('region'))
        self.add_col('Tenant', self.get_attr('tenant'))
        self.add_col('ASN', self.get_attr('asn'))
        self.add_col('Description', self.get_attr('description'))


#class DcimVirtualChassisView(BaseView):
