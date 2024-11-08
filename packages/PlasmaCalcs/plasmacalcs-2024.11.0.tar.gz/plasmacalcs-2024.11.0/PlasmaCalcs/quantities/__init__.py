"""
Package Purpose: managing the various formulae for quantities for PlasmaCalculator.
"""

from .collisions import CollisionsLoader, CrossTable
from .patterns import (
    # loaders
    ParenthesisLoader,
    BasicArithmeticLoader, BasicDerivativeLoader,
    BlurLoader, FFTLoader,
    PolyfitLoader,
    StatsLoader,
    VectorArithmeticLoader, VectorDerivativeLoader,
    # other things
    XHAT, YHAT, ZHAT,
    dot_product, magnitude, cross_product, cross_component,
    take_perp_to, take_parallel_to,
)
from .bases import (
    AllBasesLoader, SimpleDerivedLoader,
    BASE_QUANTS, SIMPLE_DERIVED_QUANTS,
)
from .bperp import BperpLoader
from .caching import CachedQuantity, VarCache
from .constants import ConstantsLoader
from . import help as _help_module
from .plasma_drifts import PlasmaDriftsLoader
from .plasma_heating import PlasmaHeatingLoader
from .plasma_parameters import PlasmaParametersLoader
from .plasma_stats import PlasmaStatsLoader
from .quasineutral import QuasineutralLoader
from .timescales import TimescalesLoader

# parent class & other tools, for the other loaders.
# Probably won't use these directly, outside of this subpackage.
from .quantity_loader import (
    MetaQuantTracking, QuantityLoader,
)
from .quantity_tools import (
    LoadableQuantity, LoadableVar, LoadablePattern,
    MatchedQuantity, MatchedVar, MatchedPattern,
    Pattern,
    DecoratingCalcs, DecoratingPatterns, DecoratingSetters,
    CallDepthMixin,
)
