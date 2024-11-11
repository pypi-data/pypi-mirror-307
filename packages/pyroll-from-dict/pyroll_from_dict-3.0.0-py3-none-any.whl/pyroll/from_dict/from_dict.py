import importlib
from inspect import isclass

import pyroll.core as pr

from .config import Config
from .explicit_functions import is_function, parse_function
from .resolve import resolve, resolve_heuristically


def dict_input(d: dict) -> tuple[pr.Profile, pr.Unit]:
    namespaces = {k: importlib.import_module(v) for k, v in d[Config.NAMESPACES_KEY].items()}

    in_profile = from_dict(d[Config.IN_PROFILE_KEY], namespaces)

    d_unit = d[Config.UNIT_KEY]
    if isinstance(d_unit, list):
        unit = pr.PassSequence([from_dict(u, namespaces) for u in d_unit])
    else:
        unit = from_dict(d_unit, namespaces)

    return in_profile, unit


def from_dict(d: dict, namespaces: dict[str, ...], name: str = None, parent: type = None) -> ...:
    factory_name = d.get(Config.FACTORY_KEY, None)
    if factory_name:
        if isinstance(factory_name, str):
            factory = resolve(factory_name, namespaces)
        elif callable(factory_name):
            factory = factory_name
        else:
            raise ValueError("The given factory must be a string identifier or a callable object.")
    else:
        factory = resolve_heuristically(d, name, parent)
    args = d.copy()
    args.pop(Config.FACTORY_KEY, None)

    cls = factory if isclass(factory) else factory.__self__

    for k, v in args.items():
        if isinstance(v, dict):
            args[k] = from_dict(v, namespaces, k, cls)
        if is_function(v):
            args[k] = parse_function(v, namespaces)

    return factory(**args)
