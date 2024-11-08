"""
File Purpose: basic tests for eppic hookup in PlasmaCalcs.
These tests require some simulation output.
They also test reading lots of different basic values,
    with lots of different values for dims & slices,
    so it takes a little while to run (~20-30 seconds?).
"""
import os
import pytest

import numpy as np

import PlasmaCalcs as pc
pc.DEFAULTS.pic_ambiguous_unit = dict(u_t=1)  # must be defined before loading an EppicCalculator.

HERE = os.path.dirname(__file__)


''' --------------------- can create eppic calculator --------------------- '''

def get_eppic_calculator(**kw_init):
    '''make an eppic calculator'''
    with pc.InDir(os.path.join(HERE, 'test_eppic_tinybox')):
        ec = pc.EppicCalculator.from_here(**kw_init)
    return ec


''' --------------------- basic tests --------------------- '''

def test_dimensions_manip():
    '''ensure can manipulate dimensions properly.'''
    ec = get_eppic_calculator()
    # snaps: there are 10 snaps: 0,1,...,9. Going from it='2560' to it='25600'
    ec.snap = None; assert ec.snap.size == 10
    ec.snap = 0; assert ec.snap.size == 1
    ec.snap = '2560'; assert ec.snap.size == 1
    ec.snap = ['5120', '7680']; assert len(ec.snap) == 2
    ec.snap = 4; assert ec.snap.size == 1
    ec.snap = slice(0, None, 2); assert ec.snap.size == 5
    ec.snap = slice(0, None, 0.4)  # check that "interprets_fractional_indexing" works as expected
    assert ec.snap == ec.snaps[slice(0, None, 3)]
    assert ec.snap.size == 4
    ec.snap = -1; assert ec.snap.size == 1
    # fluids: there are 3 fluids ('e-', 'H+', 'C+')
    ec.fluid = None; assert ec.fluid.size == 3; assert ec.fluid == ['e-', 'H+', 'C+']
    ec.fluid = 0; assert ec.fluid.size == 1; assert ec.fluid == 'e-'
    ec.fluid = -1; assert ec.fluid.size == 1; assert ec.fluid == 'C+'
    ec.fluid = 'H+'; assert ec.fluid.size == 1
    ec.fluid = ['H+', 'C+']; assert len(ec.fluid) == 2
    ec.fluid = ec.fluids.get_electron(); assert ec.fluid.size == 1
    ec.fluid = ec.fluids.charged(); assert ec.fluid.size == 3
    with pytest.raises(pc.FluidKeyError):  # eppic has no neutral fluid, only a constant background.
        ec.fluids.get_neutral()
    # components: there are 3 components ('x', 'y', 'z')
    ec.component = None; assert ec.component.size == 3; assert ec.component == ['x', 'y', 'z']
    ec.component = 0; assert ec.component.size == 1; assert ec.component == 'x'
    ec.component = 'z'; assert ec.component.size == 1
    ec.component = ['x', 'y']; assert len(ec.component) == 2
    ec.component = slice(0, None, 2); assert ec.component.size == 2
    # maindims: there are 2 maindims ('x', 'y')  (it was a 2D run) each with size 16.
    assert len(ec.maindims) == 2
    ec.slices = dict(); assert ec.maindims_shape == (16, 16); assert ec.maindims_size == 16*16
    ec.slices = dict(x=0); assert ec.maindims_shape == (1, 16); assert ec.maindims_size == 16
    ec.slices = dict(x=5); assert ec.maindims_shape == (1, 16); assert ec.maindims_size == 16
    ec.slices = dict(y=-1); assert ec.maindims_shape == (16, 1); assert ec.maindims_size == 16
    ec.slices = dict(x=0, y=0); assert ec.maindims_shape == (1, 1); assert ec.maindims_size == 1
    ec.slices = dict(x=slice(0, None, 2)); assert ec.maindims_shape == (8, 16); assert ec.maindims_size == 8*16
    ec.slices = dict(x=slice(0, 10, 2), y=slice(7, 11)); assert ec.maindims_shape == (5, 4); assert ec.maindims_size == 5*4

# takes roughly 20 seconds
def test_reading_basic_values():
    '''ensure can read basic values from eppic.'''
    # checks that output size is correct, for various dimensions.
    # use some of the same dimensions as in test_dimensions_manip, to enable hard-coding the expected results.
    # don't use all of them, because that produces hundreds of input combinations, which takes a while.
    # also compare against the dynamically-calculated expected results.
    ec = get_eppic_calculator()
    snap_inputs = [None, 4, slice(0, None, 2)]
    snap_sizes = [10, 1, 5]
    fluid_inputs = [None, -1, ['H+', 'C+']]
    fluid_sizes = [3, 1, 2]
    component_inputs = [None, 'z', ['x', 'y']]
    component_sizes = [3, 1, 2]
    slice_inputs = [dict(), dict(x=5), dict(x=0, y=0), dict(x=slice(0, 10, 2), y=slice(7, 11))]
    slice_shapes = [(16, 16), (1, 16), (1, 1), (5, 4)]
    slice_sizes = [16*16, 16, 1, 5*4]

    input_attrs = []  # list of dicts of attr values
    input_sizes = []  # list of dicts of attr sizes
    for snap, snap_size in zip(snap_inputs, snap_sizes):
        for fluid, fluid_size in zip(fluid_inputs, fluid_sizes):
            for component, component_size in zip(component_inputs, component_sizes):
                for slices, slice_size in zip(slice_inputs, slice_sizes):
                    input_attrs.append(dict(snap=snap, fluid=fluid, component=component, slices=slices))
                    input_sizes.append(dict(snap=snap_size, fluid=fluid_size, component=component_size, slice=slice_size))
    assert len(input_attrs) == len(input_sizes)
    assert len(input_attrs) == len(snap_sizes) * len(fluid_sizes) * len(component_sizes) * len(slice_sizes)

    for attrs, sizes in zip(input_attrs, input_sizes):
        ec.set_attrs(**attrs)
        # redundant with test_dimensions_manip to check size here, but these are tests so redundancy is fine.
        assert ec.current_n_snap() == sizes['snap']
        assert ec.current_n_fluid()== sizes['fluid']
        assert ec.current_n_component() == sizes['component']
        assert ec.maindims_size == sizes['slice']
        # get some basic values and assert they have the correct size.
        arr = ec('n')  # in its own line for easier debugging in case of crash.
        dynamic_expect_size = ec.match_var_result_size('n')  # dynamically calculate expected size.
        simple_expect_size = sizes['snap'] * sizes['fluid'] * sizes['slice']  # size based on the things 'n' depends on.
        assert arr.size == dynamic_expect_size == simple_expect_size
        arr = ec('E')
        dynamic_expect_size = ec.match_var_result_size('E')
        simple_expect_size = sizes['snap'] * sizes['component'] * sizes['slice']
        assert arr.size == dynamic_expect_size == simple_expect_size
        arr = ec('u')
        dynamic_expect_size = ec.match_var_result_size('u')
        simple_expect_size = sizes['snap'] * sizes['fluid'] * sizes['component'] * sizes['slice']
        assert arr.size == dynamic_expect_size == simple_expect_size
        arr = ec('Ta')
        dynamic_expect_size = ec.match_var_result_size('Ta')
        simple_expect_size = sizes['snap'] * sizes['fluid'] * sizes['component'] * sizes['slice']
        assert arr.size == dynamic_expect_size == simple_expect_size
        # get some slightly more complicated values and assert they have the correct size.
        arr = ec('E_x')
        dynamic_expect_size = ec.match_var_result_size('E_x')
        simple_expect_size = sizes['snap'] * sizes['slice']
        assert arr.size == dynamic_expect_size == simple_expect_size
        arr = ec('u_y')
        dynamic_expect_size = ec.match_var_result_size('u_y')
        simple_expect_size = sizes['snap'] * sizes['fluid'] * sizes['slice']
        assert arr.size == dynamic_expect_size == simple_expect_size
        arr = ec('T')
        dynamic_expect_size = ec.match_var_result_size('T')
        simple_expect_size = sizes['snap'] * sizes['fluid'] * sizes['slice']
        assert arr.size == dynamic_expect_size == simple_expect_size
        arr = ec('mod_E')
        dynamic_expect_size = ec.match_var_result_size('mod_E')
        simple_expect_size = sizes['snap'] * sizes['slice']
        assert arr.size == dynamic_expect_size == simple_expect_size
        arr = ec('mean_n')
        dynamic_expect_size = ec.match_var_result_size('mean_n', maindims=False)  # [TODO] infer maindims=False from 'mean'.
        simple_expect_size = sizes['snap'] * sizes['fluid']
        assert arr.size == dynamic_expect_size == simple_expect_size
        arr = ec('std_u')
        dynamic_expect_size = ec.match_var_result_size('std_u', maindims=False)  # [TODO] infer maindims=False from 'std'.
        simple_expect_size = sizes['snap'] * sizes['fluid'] * sizes['component']
        assert arr.size == dynamic_expect_size == simple_expect_size
