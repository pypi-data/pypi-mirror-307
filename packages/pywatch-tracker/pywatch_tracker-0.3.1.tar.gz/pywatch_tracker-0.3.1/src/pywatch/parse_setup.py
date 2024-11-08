import importlib
import pathlib
from types import ModuleType


def parse_module(module_name: str, file_path: str) -> ModuleType:
    mod = import_module_from_path(module_name, file_path)
    return check_module(mod)


def import_module_from_path(module_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module_ = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module_)
    return module_


def check_module(mod: ModuleType) -> ModuleType:
    """Check whether every variable in the module is set correctly.
    Set unset variable, if they are supposed to have default values."""

    if not hasattr(mod, "SIMULATION"):
        mod.SIMULATION = False
    else:
        if not isinstance(mod.SIMULATION, bool):
            raise TypeError("SIMULATION must be a boolean")

    if not hasattr(mod, "EVENT_COUNT"):
        mod.EVENT_COUNT = None
    elif not isinstance(mod.EVENT_COUNT, int) or mod.EVENT_COUNT < 1:
        raise TypeError("EVENT_COUNT must be a positive integer.")

    if not hasattr(mod, "SEGMENTATION"):
        mod.SEGMENTATION = 5
    elif not isinstance(mod.SEGMENTATION, int) or mod.SEGMENTATION < 1 or mod.SEGMENTATION % 2 != 1:
        raise TypeError("SEGMENTATION must be an odd positive integer.")

    mod = check_geometry_file(mod)

    # TODO implement simulation parsing
    if mod.SIMULATION:
        return mod
    else:
        return check_module_no_sim(mod)


def check_module_no_sim(mod: ModuleType) -> ModuleType:
    if not hasattr(mod, "PORTS"):
        raise TypeError("PORTS was not set.")
    elif not is_list_with_type(mod.PORTS, str):
        raise TypeError("PORTS must be a list of strings.")

    if not hasattr(mod, "THRESHOLD"):
        mod.THRESHOLD = 10
    elif not isinstance(mod.THRESHOLD, int) or mod.THRESHOLD < 1:
        raise TypeError("THRESHOLD must be a positive integer.")

    if not hasattr(mod, "SAVE_FILE"):
        mod.SAVE_FILE = None
    elif not isinstance(mod.SAVE_FILE, str):
        raise TypeError("SAVE_FILE must be a string.")

    return mod


def check_geometry_file(mod: ModuleType) -> ModuleType:
    if not hasattr(mod, "GEOMETRY_FILE"):
        mod.GEOMETRY_FILE = None
    elif not isinstance(mod.GEOMETRY_FILE, str):
        raise TypeError("GEOMETRY_FILE must be a string.")
    else:
        if not pathlib.Path(mod.GEOMETRY_FILE).is_file():
            raise TypeError(f"GEOMETRY_FILE not found.")

    return mod


def is_list_with_type(ls, type_) -> bool:
    if not isinstance(ls, list):
        return False

    for x in ls:
        if not isinstance(x, type_):
            return False

    return True
