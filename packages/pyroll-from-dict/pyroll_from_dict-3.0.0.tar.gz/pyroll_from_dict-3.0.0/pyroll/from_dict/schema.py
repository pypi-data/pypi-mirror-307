from collections.abc import Collection, Mapping
from dataclasses import is_dataclass
from inspect import Parameter, signature
from typing import Callable, get_args, get_origin

from schema import Optional, Or, Regex, Schema

import pyroll.core as pr
from pyroll.from_dict import Config


def create_input_schema():
    """
    Create a validation schema for a complete PyRolL input via dict, JSON, yaml or similar.

    :return: a ``schema.Schema`` instance
    """
    profile_schema = Or(
        create_schema(pr.Profile, pr.Profile.round),
        create_schema(pr.Profile, pr.Profile.diamond),
        create_schema(pr.Profile, pr.Profile.square),
        create_schema(pr.Profile, pr.Profile.box),
        create_schema(pr.Profile, pr.Profile.from_groove),
        create_schema(pr.Profile, pr.Profile.from_polygon),
        create_schema(pr.RoundProfile),
        create_schema(pr.DiamondProfile),
        create_schema(pr.SquareProfile),
        create_schema(pr.BoxProfile),
    )
    units_schemas = [
        create_schema(pr.RollPass, qualname="pr.RollPass"),
        create_schema(pr.TwoRollPass),
        create_schema(pr.ThreeRollPass),
        create_schema(pr.Transport),
        create_schema(pr.Rotator),
        create_schema(pr.PassSequence),
    ]
    schema = Schema(
        {
            Config.NAMESPACES_KEY: {str: str},
            Config.IN_PROFILE_KEY: profile_schema,
            Or(Config.UNIT_KEY, Config.SEQUENCE_KEY): Or([*units_schemas], *units_schemas),
        }
    )

    return schema


def create_schema(type: type, ctor: Callable = None, qualname= None):
    """
    Create a validation schema for a given type and constructor.

    :param type: the type to instantiate
    :param ctor: the constructor/factory method to use (equals ``t`` if omitted)
    :return: a ``schema.Schema`` instance
    """
    ctor = ctor or type
    qualname = qualname or ctor.__qualname__

    return Schema(_create_schema_for_pyroll(type, ctor, qualname))


def _analyse_ctor_arg(info: Parameter):
    name = info.name
    annotation = info.annotation

    if str(annotation).startswith("typing.Optional"):
        data_type = get_args(annotation)[0]
        required = False
    elif info.default is not Parameter.empty:
        data_type = annotation
        required = False
    else:
        data_type = annotation
        required = True
    return name, data_type, required


def _create_schema_from_constructor(ctor, qualname):
    ctor_sig = signature(ctor)
    args = [_analyse_ctor_arg(info) for arg, info in ctor_sig.parameters.items() if arg not in {"kwargs", "parent"}]
    args_schema = dict(_create_schema_for_arg(*arg) for arg in args)

    return {Optional(Config.FACTORY_KEY): Regex(rf"[\w.]*{qualname}")} | args_schema


def _create_schema_for_pyroll(t, ctor, qualname):
    ctor_schema = _create_schema_from_constructor(ctor, qualname)

    hook_args = [(name, hook.type) for name, hook in t.__dict__.items() if isinstance(hook, pr.Hook)]

    hook_schema = dict(_create_schema_for_arg(arg[0], arg[1], False) for arg in hook_args)
    return ctor_schema | hook_schema


def _create_schema_for_type(type):
    try:
        origin = get_origin(type)

        if origin is not None:
            args = get_args(type)

            if str(origin).startswith("typing.Union"):
                return Or(*[_create_schema_for_type(arg) for arg in args])

            if issubclass(origin, Callable):
                return str

            if issubclass(origin, Mapping):
                return {_create_schema_for_type(args[0]): _create_schema_for_type(args[1])}

            if issubclass(origin, Collection):
                return [_create_schema_for_type(args[0])]

        if issubclass(type, bool):
            return bool

        if issubclass(type, float):
            return Or(float, int)

        if issubclass(type, int):
            return int

        if issubclass(type, str):
            return str

        if issubclass(type, Mapping):
            return dict

        if issubclass(type, Collection):
            return list

        if issubclass(type, pr.HookHost):
            return _create_schema_for_pyroll(type, type, type.__qualname__)

        if issubclass(type, pr.GrooveBase):
            return Or(
                *[
                    _create_schema_from_constructor(g, f"pr.{n}")
                    for n, g in pr.__dict__.items()
                    if "Groove" in n and "Base" not in n
                ]
                + [{Config.FACTORY_KEY: str, str: str}]
            )

        if is_dataclass(type):
            return _create_schema_from_constructor(type)

        raise TypeError
    except TypeError:
        return {str: str}


def _create_schema_for_arg(name, type, required):
    type_schema = _create_schema_for_type(type)

    if not required:
        return Optional(name), type_schema
    return name, type_schema
