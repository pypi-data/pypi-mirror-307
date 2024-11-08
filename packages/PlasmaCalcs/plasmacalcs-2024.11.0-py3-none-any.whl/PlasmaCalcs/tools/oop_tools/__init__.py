"""
Package Purpose: Miscellaneous quality-of-life routines for Object Oriented Programming tasks.

This package is intended to provide functions which:
- are helpful for solving specific, small problems related to Object Oriented Programming.
    E.g. make an alias property, bind a function to an already existing class, caching attributes,
    [TODO] track across subclasses and access in O(1) time (rather than O(n) for n subclasses) via caching.
        (this last one is implemented in simplifiable_objects.py but a more general implementation belongs here.)
- could be useful in other projects as well
    i.e., these should not depend on other parts of SymSolver.
    (One exception: they may depend on the default values in defaults.py)

This file:
Imports the main important objects throughout this subpackage.
"""

from .binding import (
    bind_to, Binding,
)
from .manage_attrs import (
    maintaining_attrs, using_attrs,
    maintain_attrs, use_attrs,
    MaintainingAttrs, UsingAttrs,
    UsingAttrsSignaled,
    IncrementableAttrManager,
)
from .oop_misc import (
    apply,
    MetaClsRepr,
)