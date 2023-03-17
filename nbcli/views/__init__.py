"""Load views used by nbprint."""

from nbcli.views.tools import BaseView

from nbcli.views.circuits import CircuitsProvidersView
from nbcli.views.circuits import CircuitsCircuitTypesView
from nbcli.views.circuits import CircuitsCircuitsView

from nbcli.views.dcim import DcimDevicesView
from nbcli.views.dcim import DcimInterfacesView
from nbcli.views.dcim import DcimRacksView
from nbcli.views.dcim import DcimRUsView
from nbcli.views.dcim import DcimLocationsView
from nbcli.views.dcim import DcimSitesView

from nbcli.views.extras import ExtrasConfigContextsView
from nbcli.views.extras import ExtrasObjectChangesView

from nbcli.views.ipam import IpamAggregatesView
from nbcli.views.ipam import IpamIpAddressesView
from nbcli.views.ipam import IpamPrefixesView
from nbcli.views.ipam import IpamVlansView

from nbcli.views.tenancy import TenancyTenantGroupsView
from nbcli.views.tenancy import TenancyTenantsView
