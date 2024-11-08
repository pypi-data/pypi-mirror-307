"""
File Purpose: misc tests for eppic hookup in PlasmaCalcs.
These tests require some simulation output.
Not intended to read lots of different values,
    just to read a few specific/misc. values to check if they work properly.
"""
import os
import pytest

import numpy as np
import xarray as xr

import PlasmaCalcs as pc
pc.DEFAULTS.pic_ambiguous_unit = dict(u_t=1)  # must be defined before loading an EppicCalculator.

HERE = os.path.dirname(__file__)


''' --------------------- can create eppic calculator --------------------- '''

def get_eppic_calculator(**kw_init):
    '''make an eppic calculator'''
    with pc.InDir(os.path.join(HERE, 'test_eppic_tinybox')):
        ec = pc.EppicCalculator.from_here(**kw_init)
    return ec

def test_make_eppic_calculator():
    '''ensure can make an eppic calculator (with various inputs to __init__).'''
    get_eppic_calculator()
    get_eppic_calculator(snaps_from='timers')
    get_eppic_calculator(kw_units=dict(M=1))


''' --------------------- runtimes --------------------- '''

def test_reading_runtimes():
    '''test reading runtimes from eppic timers.dat'''
    ec = get_eppic_calculator()
    with pytest.raises(ValueError):
        ec('runtimes')  # fails because snap 0 file was deleted but timer is known for it.
    ec = get_eppic_calculator(snaps_from='timers')
    arr = ec('runtimes')  # just checking that this doesn't crash!
    arr = ec('calc_timestep_cost')
    assert arr.size == len(ec.snap)


''' --------------------- multi_slices --------------------- '''

def test_reading_multi_slices():
    '''test reading when using multi_slices.
    Also confirms Dataset.pc.size works properly.
    '''
    ec = get_eppic_calculator()
    with ec.using(multi_slices=dict(ndim=1, ikeep=0)):
        ds = ec('n')
    with ec.using(slices=dict(x=0)):
        arr_x0 = ec('n')
    with ec.using(slices=dict(y=0)):
        arr_y0 = ec('n')
    assert np.all(ds['keep_x'] == arr_y0)  # keep x <--> used y=0 slice
    assert np.all(ds['keep_y'] == arr_x0)  # keep y <--> used x=0 slice
    assert ds.pc.size == arr_x0.pc.size + arr_y0.pc.size


''' --------------------- multiprocessing + parenthesis --------------------- '''

def test_mp_timeout():
    '''ensure eppic calculator will timeout properly.'''
    ec = get_eppic_calculator()
    ec.snap = [i%10 for i in range(10000)]  # a lot of snapshots (to make it take longer to read)
    longvar = 'stats_lowpass_(u_drift**2)'  # something that takes a while to calculate
    # assumes these calculations would take >1 second --> timeout = 1s must cause timeout crash.
    with pytest.raises(pc.TimeoutError):
        ec(longvar, ncpu=1, timeout=1)   # ensure timeout works when ncpu=1
    assert len(ec.snap) == 10000  # ensure original snaps restored even after TimeoutError.
    with pytest.raises(pc.TimeoutError):
        ec(longvar, ncpu=2, timeout=1)   # ensure timeout works when ncpu>1

# takes roughly 7 seconds
def test_mp_with_parenthesis():
    '''ensure can run multiprocessing with parenthesis.'''
    # it can be tricky because parenthesis_memory is a class variable,
    # and pickling doesn't include changes to class or global variables, by default.
    # this ensures that the __getstate__ & __setstate__ solution works properly
    ec = get_eppic_calculator()
    ec.ncpu = 2
    ec('(n0)')
    ec('(deltafrac_n+1)*7')
    ec('mean_(n)')
    ec('nmean_(u**2)', stats_dimpoint_wise=False)
    ec('nmean_(u**2)', stats_dimpoint_wise=True)
