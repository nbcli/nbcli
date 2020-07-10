"""Initialize nbcli module."""

from pynetbox.models.dcim import Interfaces
from nbcli.__version__ import __version__  # noqa: F401
from nbcli.core.utils import add_detail_endpoint, get_nbcli_logger, Trace


logger = get_nbcli_logger()

# Add Detail Endpoints that are not included in pynetbox
add_detail_endpoint(Interfaces, 'trace', RO=True, custom_return=Trace)
