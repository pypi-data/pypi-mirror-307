"""
Package Purpose: dimensions affecting plasma quantity results
E.g. "first fluid", "vector component axis", "second fluid"
"""
# behaviors
from .behavior import Behavior, BehaviorQuantity, BehaviorHaver
# the DimensionHavers
from .components import Component, ComponentList, ComponentHaver
from .fluids import (
    Fluid, FluidList,
    UniqueFluid, SINGLE_FLUID,
    FluidSpecialValueSetter,
    SET_CHARGED, SET_ELECTRON, SET_ELECTRONS, SET_ION, SET_IONS, SET_NEUTRAL, SET_NEUTRALS,
    FluidDimension, FluidHaver,
    jFluidDimension, jFluidHaver,
    FluidsHaver,
)
from .main_dimensions import MainDimensionsHaver
from .runs import Run, RunList, RunHaver, _paramdocs_runs
from .snaps import (
    Snap, SnapList, SnapDimension, SnapHaver,
    UniqueSnap, INPUT_SNAP, MISSING_SNAP,
    ProxySnap, ProxySnapList,
    SELECT_CLOSEST, SELECT_BEFORE, SELECT_AFTER,
    SELECT_ALL_BEFORE, SELECT_ALL_AFTER, SELECT_BETWEEN,
)
from .subsampling import (
    SubsamplingInfo, Subsamplable,
    SubsamplingInfoPathManager, SubsamplingResultPathManager,
    SubsamplingApplier, SubsamplingSlice,
)

# parent class & other tools, for the other dimension havers.
# Probably won't use these directly, outside of this subpackage.
from .dimension_tools import (
    DimensionValue, SliceableList,
    DimensionValueList, string_int_lookup,
    DimensionValueSetter, UniqueDimensionValue,
    Dimension,
    DimensionHaver,
    xarray_save, xarray_load,
)

# miscellaneous other stuff
from .components import XYZ, YZ_FROM_X
