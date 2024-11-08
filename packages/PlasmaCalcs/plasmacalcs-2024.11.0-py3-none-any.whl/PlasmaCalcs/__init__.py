"""Consistent interface for plasma calculations from any inputs.

[TODO] more details about PlasmaCalcs here.
"""
#[TODO] explicit imports instead of *

__version__ = '2024.11.0'  # YYYY.MM.MICRO  # MM not 0M, to match pip normalization.

from .dimensions import *
from .hookups import *
from .multi_run_analysis import *
from .plotting import *
from .quantities import *
from .units import *
from .tools import *

from .defaults import DEFAULTS
from .errors import *
from .plasma_calculator import (
    DimensionlessPlasmaCalculator,
    PlasmaCalculator, MultifluidPlasmaCalculator,
)
