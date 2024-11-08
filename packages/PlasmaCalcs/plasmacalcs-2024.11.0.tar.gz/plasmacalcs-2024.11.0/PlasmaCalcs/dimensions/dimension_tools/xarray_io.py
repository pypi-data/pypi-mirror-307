"""
File Purpose: tools for saving & loading xarrays that have Dimension coordinates
xarray can be saved by default via to_netcdf().
But that fails when coords are custom objects (like Dimensions).
These methods help to handle that issue!
"""
import ast
import os

import numpy as np
import xarray as xr

from .dimension_value import DimensionValue
from ...errors import DimensionError
from ...tools import (
    format_docstring,
    pcAccessor,
)


@pcAccessor.register('save')  # <-- tells xr.DataArray.pc.save to call xarray_save
def xarray_save(array, filename=None, *, exist_ok=False):
    '''saves the array or dataset as filename.nc with a companion text file filename.txt.
    Both will be saved into a new directory named filename.pcxarr
    ("pcxarr" stands for "PlasmaCalcs xarray.DataArray or xarray.Dataset object")

    array: xarray.DataArray or xarray.Dataset
        the array or dataset to save
    filename: None or str
        where to save the array. Extension ".pcxarr" will be added if not present.
        None --> infer filename=array.name, or "unnamed_array" if array.name is None.
                (actually: array.name.replace('/', '÷'). To avoid interpreting division as directories.)
        if filename implies directories, those directories will be created, as per os.makedirs.
    exist_ok: bool, default False
        whether it's okay directory with the target name to already exist.
        False --> crash with FileExistsError if directory exists.
        True --> might overwrite files in that directory!

    returns abspath to filename.pcxarr directory where the array was saved.
    '''
    # filename/bookkeeping
    if filename is None:
        if array.name is None:
            filename = "unnamed_array"
        else:
            filename = array.name.replace('/', '÷')  # slashes in array name represent division, not file paths!
    if not filename.endswith('.pcxarr'):
        filename += '.pcxarr'
    if os.path.exists(filename):
        if not exist_ok:
            raise FileExistsError(f"Directory {filename} already exists; use a different name or set exist_ok=True.")
    else:
        os.makedirs(filename, exist_ok=True)  # already checked exist_ok=False case above^, so use True here.
    filename = os.path.abspath(filename)
    basename = os.path.splitext(os.path.basename(filename))[0]
    netcdf_filename = f"{filename}/{basename}.nc"
    text_filename = f"{filename}/{basename}.txt"
    # serializing coords made of DimensionValue objects.
    serializations = dict()
    for cname, carr in array.coords.items():  # carr is the array of value(s) of this coord.
        xx = carr.values  # xx is carr as a numpy array.
        if isinstance(xx.flat[0], DimensionValue):
            # need to serialize, & will need to remove this coord.
            if xx.ndim == 0:
                serializations[cname] = xx.flat[0].serialize()
            elif xx.ndim == 1:
                serializations[cname] = [x.serialize() for x in xx]  # [TODO] DimensionValueList(xx).serialize() instead?
            else:
                errmsg = (f"serialization of 2D+ DimensionValue coords not yet implemented."
                         f"(cname={cname!r}; ndim={xx.ndim}.)")
                raise DimensionError(errmsg)
    # drop serialized coords from array, save results.
    array = array.drop_vars(list(serializations.keys()))
    array.to_netcdf(netcdf_filename)
    # record whether array was a DataArray or Dataset, save results.
    serializations['xarray_object_type'] = type(array).__name__
    with open(text_filename, 'w') as f:
        print(serializations, file=f)
    # return the directory where the array was saved.
    return filename

def xarray_load(filename, **kw__xarray_open):
    '''load the array or dataset from filename.pcxarr.
    filename: str
        where to load the array from. Extension ".pcxarr" will be added if not present.

    additional kwargs go to xarray.open_dataarray, or xarray.open_dataset
    '''
    # filename/bookkeeping
    if not filename.endswith('.pcxarr'):
        filename += '.pcxarr'
    basename = os.path.splitext(os.path.basename(filename))[0]
    netcdf_filename = f"{filename}/{basename}.nc"
    text_filename = f"{filename}/{basename}.txt"
    # load xarray type & coords info from text file then deserialize:
    with open(text_filename, 'r') as f:
        serial = ast.literal_eval(f.read())
    xarray_object_type = serial.pop('xarray_object_type', 'DataArray')  # default DataArray for backwards compatibility
    coords = dict()
    for cname, cserial in serial.items():
        if isinstance(cserial, dict):  # 0d coord
            coords[cname] = DimensionValue.deserialize(cserial)
        elif isinstance(cserial, list):  # 1d coord
            coords[cname] = [DimensionValue.deserialize(x) for x in cserial]
        else:
            raise DimensionError(f"unexpected serialization type for coord {cname!r}: {type(cserial)}")
    # load array or dataset from netcdf file:
    if xarray_object_type == 'DataArray':
        array = xr.open_dataarray(netcdf_filename, **kw__xarray_open)
    elif xarray_object_type == 'Dataset':
        array = xr.open_dataset(netcdf_filename, **kw__xarray_open)
    else:
        raise DimensionError(f"unexpected xarray_object_type {xarray_object_type!r}, from {text_filename!r}.")
    # assign coords to array or dataset:
    array = array.assign_coords(coords)
    return array
