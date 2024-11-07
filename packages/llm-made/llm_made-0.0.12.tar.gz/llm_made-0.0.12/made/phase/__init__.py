import importlib
import pkgutil

from made.utils.registry import Registry


PhaseRegistry = Registry("Phase")


def import_all_modules(package_name):
    package = importlib.import_module(package_name)
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)
        if is_pkg:
            import_all_modules(full_module_name)


import_all_modules("made.phase.repository")