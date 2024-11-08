"""
File Purpose: testing some parts of plotting code.
"""
import os

import matplotlib.pyplot as plt
import numpy as np
import pytest
import xarray as xr

import PlasmaCalcs as pc

# ARTIFACTS STUFF:
HERE = os.path.dirname(__file__)
TESTS_DIR = HERE
ARTIFACTS = os.path.join(TESTS_DIR, '_test_artifacts', 'plots')
if os.path.exists(ARTIFACTS):  # remove any plots artifacts before running tests.
    import shutil; shutil.rmtree(ARTIFACTS)
os.makedirs(ARTIFACTS)


def savefig_and_close(name, *, bbox_inches='tight', **kw):
    '''savefig to ARTIFACTS/name, then plt.close().'''
    plt.savefig(os.path.join(ARTIFACTS, name), bbox_inches='tight', **kw)
    plt.close()

def test_plot_settings_cls():
    '''testing the PlotSettings class'''
    keys = list(pc.PlotSettings.MPL_KWARGS.keys())
    assert len(keys) > 0   # i.e., this test isn't pointless...
    assert len(keys) > 5   # there are more than 5 keys at time of writing this test.
    for key in keys:
        vals = pc.PlotSettings.get_mpl_keys(key)  # ensure this doesn't crash
        assert len(vals) > 0         # and this key points to at least 1 kwarg.

    ps = pc.PlotSettings(squeeze=True, figsize=(10, 10), dpi=100, fontsize=12, aspect=1)
    kw = ps.get_mpl_kwargs('fig.subplots')
    assert kw['squeeze'] is True
    assert kw['subplot_kw']['aspect'] == 1
    assert all(key not in kw for key in ('dpi', 'figsize', 'fontsize')) # these cannot be passed to fig.subplots.
    # note, kw might contain other values if defaults have changed since this test was written.
    kw = ps.get_mpl_kwargs('plt.figure')
    default_layout = ps.get_default('layout')  # layout is one of the figure kwargs with a default value.
    assert kw['layout'] == default_layout
    assert kw['figsize'] == (10, 10)
    assert kw['dpi'] == 100
    assert all(key not in kw for key in ('squeeze', 'fontsize')) # these cannot be passed to plt.figure.

def test_plot_locations():
    '''tests that plot_locations() & plot_note() works! Also tests ax_remove_ticks().
    Also produce artifact that can be checked by eye later & used as a reference for locations.
    '''
    locations = pc.plot_locations()   # dict of {loc: {'xy': (x,y), 'ha': str, 'va': str}}
    for loc in locations:
        # use 'here:\n' to make multiline comment to confirm proper va.
        # don't need to test locations[loc] values because plot_note also uses plot_locations().
        pc.plot_note('here:\n'+loc, loc)
    pc.ax_remove_ticks()
    savefig_and_close('test_plot_locations.png')

def test_xarray_timelines():
    '''test that xarray timelines doesn't crash...
    also produce artifacts that could be checked by eye later.
    '''
    pc.plot_note('''test_xarray_timelines plot00, check:
        4 lines with 7 points each; slope=4;
        offset = 0, 1, 2, 3; t = 0, 1, 2, 3, 4, 5, 6;
        colors vary with offset; markers are 'o'.''')
    arr00 = xr.DataArray(np.arange(7*4).reshape(7, 4), dims=['t', 'offset'])
    tls00 = arr00.pc.timelines(marker='o')
    savefig_and_close('test_xarray_timelines_00.png')
    # plot 01: like plot 00 but all lines are blue & markers vary.
    pc.plot_note('''test_xarray_timelines plot01, check:
        4 lines with 7 points each; slope=4;
        markers vary with offset; all lines are blue.''')
    tls01 = arr00.pc.timelines(cycles=[dict(marker=['o', 'x', '+', 's'])], color='blue')
    savefig_and_close('test_xarray_timelines_01.png')
    # plot 02: like plot 00 but t varies from 0 to 1. Also ensure adding misc coord is fine!
    pc.plot_note('''test_xarray_timelines plot02, check:
        4 lines with 7 points each; t varies from 0 to 1.''')
    arr02 = xr.DataArray(np.arange(7*4).reshape(7, 4), dims=['t', 'offset'],
                        coords=dict(t=np.linspace(0, 1, 7), misc_coord='wow'))
    tls02 = pc.XarrayTimelines(arr02, marker='o')  # ensure pc.XarrayTimelines(arr) syntax works too!
    assert np.all(pc.get_data_interval('x') == np.array([0,1]))  # ensure x-axis is 0 to 1.
    savefig_and_close('test_xarray_timelines_02.png')
    # plot 10: similar idea to plot00 but introduce a third dimension (shift)
    pc.plot_note('''test_xarray_timelines plot10, check:
        12 lines with 7 points each; slope=4;
        colors vary with offset;
        linestyles vary with shift.''')
    arr10 = xr.DataArray(np.arange(7*4*3).reshape(7, 4, 3), dims=['t', 'offset', 'shift'])
    tls10 = arr10.pc.timelines()
    savefig_and_close('test_xarray_timelines_10.png')

def test_xarray_image_gif():
    '''test that XarrayImage doesn't crash when making gif...
    also produce artifacts that could be checked by eye later.
    '''
    pc.plot_note('''test_xarray_image_gif plot00, check:
        10x20 image, 8 frames; t varies 0 to 2*pi;
        x varies 0 to 2*pi; y varies 0 to 4*pi;
        waves go lower left (0,0) to upper right;
        final frame (t=2*pi) = first frame (t=0).''',
        'outside upper left', margin=0.15, fontsize='small')
    coords = {'x': np.linspace(0, 2*np.pi, 10),
              'y': np.linspace(0, 4*np.pi, 20),
              't': np.linspace(0, 2*np.pi, 8)}
    xx = xr.DataArray(coords['x'], coords=dict(x=coords['x']))
    yy = xr.DataArray(coords['y'], coords=dict(y=coords['y']))
    tt = xr.DataArray(coords['t'], coords=dict(t=coords['t']))
    data = np.sin(xx + yy - tt)
    xim = data.pc.image(title='t={t:.2f}')
    xim.save(os.path.join(ARTIFACTS, 'test_xarray_image_gif_00.gif'), fps=10)

# [TODO] how to tell gitlab to render mp4?
# def test_xarray_image_mp4():
#     '''test that XarrayImage doesn't crash when making mp4...
#     also produce artifacts that could be checked by eye later.

#     mp4 separate from gif in case one of them crashes
#     '''
#     pc.plot_note('''test_xarray_image_mp4 plot00, check:
#         10x20 image, 8 frames; t varies 0 to 2*pi;
#         x varies 0 to 2*pi; y varies 0 to 4*pi;
#         waves go lower left (0,0) to upper right;
#         final frame (t=2*pi) = first frame (t=0).''',
#         'outside upper left', margin=0.15, fontsize='small')
#     coords = {'x': np.linspace(0, 2*np.pi, 10),
#               'y': np.linspace(0, 4*np.pi, 20),
#               't': np.linspace(0, 2*np.pi, 8)}
#     xx = xr.DataArray(coords['x'], coords=dict(x=coords['x']))
#     yy = xr.DataArray(coords['y'], coords=dict(y=coords['y']))
#     tt = xr.DataArray(coords['t'], coords=dict(t=coords['t']))
#     data = np.sin(xx + yy - tt)
#     xim = data.pc.image(title='t={t:.2f}')
#     xim.save(os.path.join(ARTIFACTS, 'test_xarray_image_mp4_00.mp4'), fps=10)

def test_faceplot():
    '''test that Faceplot doesn't crash when making gif...
    also produce artifacts that could be checked by eye later.
    '''
    # create "dataset":
    coords = {'x': np.linspace(0, 4*np.pi, 20),
          'y': np.linspace(0, 2*np.pi, 10),
          'z': np.linspace(0, 2*np.pi, 10),
          't': np.linspace(0, 2*np.pi, 8)}
    xx = xr.DataArray(coords['x'], coords=dict(x=coords['x']))
    yy = xr.DataArray(coords['y'], coords=dict(y=coords['y']))
    zz = xr.DataArray(coords['z'], coords=dict(z=coords['z']))
    tt = xr.DataArray(coords['t'], coords=dict(t=coords['t']))
    data = dict()
    data['x_y'] = np.sin(xx + yy + 0 - tt)
    data['x_z'] = np.sin(xx + 0 + zz - tt)
    data['y_z'] = np.sin(0 + yy + zz - tt)
    data = xr.Dataset(data)
    # plot00: test that faceplot works
    fp = data.pc.faceplot(title='t={t:.2f}')
    pc.plot_note('''test_faceplot plot00, check:
        x varies 0 to 4*pi;  y,z,t vary 0 to 2*pi;
        waves move away from origin (0,0,0);
        final frame (t=2*pi) = first frame (t=0).''',
        'upper center', fontsize='small')
    fp.save(os.path.join(ARTIFACTS, 'test_faceplot_00.gif'), fps=10)
    # plot01: should produce same result as plot00, but the input is full 3D data;
    #   ensures that "infer faces from 3D data" works properly.
    data = np.sin(xx + yy + zz - tt)
    fp = data.pc.faceplot(title='t={t:.2f}')
    pc.plot_note('''test_faceplot plot01, check:
        x varies 0 to 4*pi;  y,z,t vary 0 to 2*pi;
        waves move away from origin (0,0,0);
        final frame (t=2*pi) = first frame (t=0).''',
        'upper center', fontsize='small')
    fp.save(os.path.join(ARTIFACTS, 'test_faceplot_01.gif'), fps=10)

def test_xarray_line():
    '''test that XarrayLine & XarrayLines don't crash...
    also produce artifacts taht could be checked by eye later.
    '''
    # plot00: test that XarrayLine works
    pc.plot_note('''test_xarray_line plot00, check:
        x varies 0 to 4*pi; t varies 0 to 2*pi;
        waves move left to right; marker='o';
        final frame (t=2*pi) = first frame (t=0).''',
        fontsize='small', fontweight='bold')
    coords = {'x': np.linspace(0, 4*np.pi, 20),
              't': np.linspace(0, 2*np.pi, 8)}
    xx = xr.DataArray(coords['x'], coords=dict(x=coords['x']))
    tt = xr.DataArray(coords['t'], coords=dict(t=coords['t']))
    data = np.sin(xx - tt)
    xline = data.pc.line(title='t={t:.2f}', marker='o')
    xline.save(os.path.join(ARTIFACTS, 'test_xarray_line_00.gif'), fps=10)
    # plot10: test that XarrayLines works.
    pc.plot_note('''test_xarray_line plot10, check:
        x varies 0 to 4*pi; t varies 0 to 2*pi;
        waves move left to right;
        final frame (t=2*pi) = first frame (t=0);
        3 similar waves offset by 2, 0, -1;
        legend tells offset for each line.''',
        fontsize='small', fontweight='bold')
    coords = {'x': np.linspace(0, 4*np.pi, 20),
              't': np.linspace(0, 2*np.pi, 8),
              'offset': np.array([2, 0, -1])}
    xx = xr.DataArray(coords['x'], coords=dict(x=coords['x']))
    tt = xr.DataArray(coords['t'], coords=dict(t=coords['t']))
    oo = xr.DataArray(coords['offset'], coords=dict(offset=coords['offset']))
    data = oo + np.sin(xx - tt)
    xlines = data.pc.lines(title='t={t:.2f}') # label='offset={offset}'
    xlines.save(os.path.join(ARTIFACTS, 'test_xarray_line_10.gif'), fps=10)
    # ensure that we raise DimensionError if too many dimensions for XarrayLine (singular)
    with pytest.raises(pc.DimensionError):
        data.pc.line()  # singular! But data has 3 dims --> wrong shape for only 1 line.
