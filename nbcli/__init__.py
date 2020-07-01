"""Initialize nbcli module."""

from pynetbox.models.dcim import Interfaces
from .__version__ import __version__  # noqa: F401
from .core.utils import add_detail_endpoint, Trace

# Add Detail Endpoints that are not included in pynetbox
add_detail_endpoint(Interfaces, 'trace', RO=True, custom_return=Trace)
