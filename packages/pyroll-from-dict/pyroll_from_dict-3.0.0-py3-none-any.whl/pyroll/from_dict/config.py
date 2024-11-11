import pyroll.core as pr


@pr.config("PYROLL_FROM_DICT")
class Config:
    FACTORY_KEY = "__ctor__"
    """Defines the key used to store the name of the factory function used to construct an object when importing dicts."""

    NAMESPACES_KEY = "namespaces"

    IN_PROFILE_KEY = "in_profile"

    UNIT_KEY = "unit"

    SEQUENCE_KEY = "sequence"
