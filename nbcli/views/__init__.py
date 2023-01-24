"""Load views used by nbprint."""

from nbcli.views.tools import BaseView                          # noqa: F401

from nbcli.views.circuits import CircuitsProvidersView          # noqa: F401
from nbcli.views.circuits import CircuitsCircuitTypesView       # noqa: F401
from nbcli.views.circuits import CircuitsCircuitsView           # noqa: F401

from nbcli.views.dcim import DcimDevicesView                  	# noqa: F401
from nbcli.views.dcim import DcimInterfacesView           		# noqa: F401
from nbcli.views.dcim import DcimRacksView        				# noqa: F401
from nbcli.views.dcim import DcimRUsView        				# noqa: F401
from nbcli.views.dcim import DcimLocationsView             		# noqa: F401
from nbcli.views.dcim import DcimSitesView                     	# noqa: F401

from nbcli.views.extras import ExtrasConfigContextsView  		# noqa: F401
from nbcli.views.extras import ExtrasObjectChangesView  		# noqa: F401

from nbcli.views.ipam import IpamAggregatesView           		# noqa: F401
from nbcli.views.ipam import IpamIpAddressesView        		# noqa: F401
from nbcli.views.ipam import IpamPrefixesView            		# noqa: F401
from nbcli.views.ipam import IpamVlansView            		    # noqa: F401

from nbcli.views.tenancy import TenancyTenantGroupsView         # noqa: F401
from nbcli.views.tenancy import TenancyTenantsView              # noqa: F401
