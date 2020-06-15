"""Initialize netbox-client module."""

from pynetbox.models.dcim import Interfaces, Racks, RUs
from .__version__ import __version__  # noqa: F401
from .core import add_detail_endpoint, Trace

# Add Detail Endpoints that are not included in pynetbox
add_detail_endpoint(Racks, 'elevation', RO=True, custom_return=RUs)
add_detail_endpoint(Interfaces, 'trace', RO=True, custom_return=Trace)
