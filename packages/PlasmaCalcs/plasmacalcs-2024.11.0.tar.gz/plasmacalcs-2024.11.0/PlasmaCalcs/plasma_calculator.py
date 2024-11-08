"""
File Purpose: The main calculator class, for hookups to inherit from.

Subclassing order recommendation:
    put the PlasmaCalculator class LAST in the order, to ensure methods from subclass are used.
    E.g. class HookupCalculator(FooLoader, BarLoader, QuuxHaver, PlasmaCalculator).
"""

from .dimensions import (
    ComponentHaver, FluidsHaver, SnapHaver,
    MainDimensionsHaver,
)
from .quantities import (
    # bases:
    AllBasesLoader, SimpleDerivedLoader,
    # misc:
    BperpLoader,
    CollisionsLoader,
    ConstantsLoader,
    PlasmaDriftsLoader, PlasmaHeatingLoader, PlasmaParametersLoader,
    PlasmaStatsLoader,
    QuasineutralLoader,
    TimescalesLoader,
    # patterns, especially stats, arithmetic, calculus:
    ParenthesisLoader,
    BlurLoader,
    FFTLoader,
    PolyfitLoader,
    StatsLoader,
    BasicArithmeticLoader, BasicDerivativeLoader,
    VectorArithmeticLoader, VectorDerivativeLoader,
)
from .units import UnitsHaver, CoordsUnitsHaver

class DimensionlessPlasmaCalculator(
                        UnitsHaver,   # units come first since they are used by some loaders
                        ParenthesisLoader,   # check for parenthesis before other patterns
                        AllBasesLoader, SimpleDerivedLoader,
                        BperpLoader,
                        ConstantsLoader,
                        # drifts & heating inherits from parameters loader, so they must come first:
                        PlasmaDriftsLoader, PlasmaHeatingLoader, PlasmaParametersLoader,
                        PlasmaStatsLoader,  # inherits from StatsLoader, so must come first.
                        QuasineutralLoader,
                        TimescalesLoader,
                        # pattern-based loaders go after bases loaders.
                        BlurLoader,
                        FFTLoader,
                        PolyfitLoader,
                        StatsLoader,
                        BasicArithmeticLoader, BasicDerivativeLoader,
                        VectorArithmeticLoader, VectorDerivativeLoader,
                       ):
    '''class for plasma calculator object.

    Not intended for direct instantiation. Instead, see options in the "hookups" subpackage,
        or write your own hookup for a different type of input, following the examples there.
    '''
    # note: the order of Loader classes *does* matter;
    #  will look in earlier classes for implementations first.
    #  e.g. if PlasmaCalculator(..., classA, ..., classB, ...) and classA and classB
    #       both have a get_foo method, then classA.get_foo will be used.
    pass

class PlasmaCalculator(CoordsUnitsHaver, MainDimensionsHaver, ComponentHaver, SnapHaver,
                       DimensionlessPlasmaCalculator):
    '''DimensionlessPlasmaCalculator but added dimensions: main dimensions, components, snaps.

    Not intended for direct instantiation. Instead, see options in the "hookups" subpackage,
        or write your own hookup for a different type of input, following the examples there.
    '''
    pass

class MultifluidPlasmaCalculator(CollisionsLoader, FluidsHaver,
                                 PlasmaCalculator):
    '''PlasmaCalculator, also with fluid and jfluid.

    Not intended for direct instantiation. Instead, see options in the "hookups" subpackage,
        or write your own hookup for a different type of input, following the examples there.
    '''
    # CollisionsLoader goes here since it depends on jfluid.
    pass
