import pyroll.core as pr
from pyroll.from_dict import Config


def resolve(name: str, namespaces: dict[str, ...] = None) -> type:
    if namespaces is None:
        namespaces = {}
    namespace = None
    object_name = None

    for key in namespaces.keys():
        if name.startswith(key):
            namespace = namespaces[key]
            object_name = name[len(key) + 1 :]
            break

    if not namespace:
        namespace = pr
        object_name = name

    for attr in object_name.split("."):
        namespace = getattr(namespace, attr)

    return namespace


def resolve_heuristically(d: dict[str, ...], name: str, parent: type):
    if "roll" in d:
        return pr.RollPass

    if "groove" in d:
        return pr.Roll

    if "duration" in d:
        return pr.Transport

    if "rotation" in d:
        return pr.Rotator

    if "units" in d:
        return pr.PassSequence

    if "radius" in d or "diameter" in d:
        return pr.Profile.round

    if "side" in d or "diagonal" in d:
        return pr.Profile.square

    if name and parent:
        target = getattr(parent, name, None)
        if target is not None and isinstance(target, pr.Hook):
            return target.type

    raise ValueError(
        "Constructor could not been determined by heuristic, "
        f"give the constructor explicitly by using the {Config.FACTORY_KEY} keyword.\n\n"
        f"name: {name}\ndata: {d}"
    )
