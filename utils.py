from typing import *


class ConnectionAlertLevel(IntEnum):
    RAISE = 1
    LOG = 2
    SUPPRESS = 3


class Module:
    def __init__(self, code: str, preclusions: Optional[Collection[str]] = None,
                 prerequisites: Optional[Collection[str]] = None, corequisites: Optional[Collection[str]] = None):
        self.code = code
        self.preclusions = preclusions if preclusions else []
        self.prerequisites = prerequisites if prerequisites else []
        self.corequisites = corequisites if corequisites else []

    def __repr__(self):
        return self.code

    def __str__(self):
        return self.code

    def __eq__(self, other):
        if isinstance(other, Module):
            return self.code == other.code

        return False

    def __hash__(self):
        return hash(self.code)