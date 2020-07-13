import importlib
import pkgutil
from pathlib import Path
import sys
from nbcli import logger


def load_extensions():

    sys.path.append(str(Path.home().joinpath('.nbcli').joinpath('user_extensions')))

    extensions = list()

    for _, name, _ in pkgutil.iter_modules():
        if name.startswith('nbcli_'):
            extensions.append(name)

    extensions.append('user_views')
    extensions.append('user_commands')

    for ext in extensions:

        try:
            importlib.import_module(ext)
            logger.info('%s loaded.', ext)
        except Exception as e:
            logger.error('Error loading %s!', ext)
            logger.error('%s: %s', type(e).__name__, str(e))
            if 0 < logger.level <= 10:
                raise e
