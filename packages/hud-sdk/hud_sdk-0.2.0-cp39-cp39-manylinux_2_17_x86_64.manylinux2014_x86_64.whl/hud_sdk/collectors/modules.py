import sys

from ..logging import internal_logger
from ..schemas.events import LoadedModules


def importlib_modules() -> LoadedModules:
    loaded_modules = []
    from importlib import metadata

    for d in metadata.distributions():
        try:
            loaded_modules.append(
                LoadedModules.ModuleData(d.metadata["Name"], d.version)
            )
        except Exception:
            internal_logger.warning("Failed to get metadata for module", exc_info=True)
    return LoadedModules(loaded_modules)


def naive_modules() -> LoadedModules:
    loaded_modules = []

    items = list(sys.modules.items())
    for module_name, module in items:
        version = getattr(module, "__version__", None)
        if version:
            version = str(version)
        loaded_modules.append(LoadedModules.ModuleData(module_name, version))
    return LoadedModules(loaded_modules)


def get_loaded_modules() -> LoadedModules:
    try:
        # Supported in Python 3.8+
        return importlib_modules()
    except Exception:
        internal_logger.debug(
            "Failed to get loaded modules using importlib", exc_info=True
        )
    return naive_modules()
