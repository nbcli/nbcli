"""Initialize nbcli module."""

from nbcli.__version__ import __version__  # noqa: F401
from nbcli.core.utils import get_nbcli_logger


logger = get_nbcli_logger()
