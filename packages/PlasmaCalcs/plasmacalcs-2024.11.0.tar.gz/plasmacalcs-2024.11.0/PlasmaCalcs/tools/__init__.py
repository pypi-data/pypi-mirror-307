"""
Package purpose: misc tools; portable (not specific to PlasmaCalcs).
"""
from .array_select import (
    select_i_closest, select_closest,
    select_i_before, select_before,
    select_i_after, select_after,
    select_i_between, select_between,
    ArraySelectable, ArraySelectableChildHaver,
)
from .arrays import (
    memory_size_check, memory_size_check_loading_arrays_like,
    finite_op, finite_min, finite_mean, finite_max, finite_std,
    finite_median, finite_percentile,
    unique_close,
    interprets_fractional_indexing,
    looks_flat, nest_shape,
)
from .display import (
    repr_simple,
    print_clear, help_str,
    join_strs_with_max_line_len,
)
from .history import (
    git_hash_local, git_hash, git_hash_here, git_hash_PlasmaCalcs,
    _PlasmaCalcs_version,
    datetime_now,
    code_snapshot_info,
)
from .fft_tools import (
    # array_fft
    fftN, fft2, fft1, fftfreq_shifted,
    ifftN, ifftfreq_shifted,
    # fft_dimnames
    FFTDimname,
    # fft_slices
    FFTSlices,
    # xarray_fft
    xarray_fftN,
    xarray_ifftN,
    xarray_lowpass,
)
from .imports import (
    enable_reload, reload,
    import_relative,
    ImportFailed,
)
from .io_tools import (
    attempt_literal_eval, read_idl_params_file,
)
from .iterables import (
    is_iterable,
    argmax, rargmax,
    DictlikeFromKeysAndGetitem,
    Partition,
    Container, ContainerOfList, ContainerOfArray, ContainerOfDict,
    Bijection, BijectiveMemory,
    SymmetricPairMapping,
    DictOfSimilar,
)
from .math import (
    ast_math_eval,
    round_to_int, float_rounding,
    is_integer,
    product, nonempty_product,
    np_all_int,
    as_roman_numeral, from_roman_numeral,
)
from .multiprocessing import (
    Task,
    CrashIfCalled, UniqueTask, UNSET_TASK, identity, IdentityTask,
    TaskContainer, TaskList, TaskArray,
    TaskContainerCallKwargsAttrHaver,
    TaskGroup, TaskPartition,
    mptest_add100, mptest_sleep, mptest_sleep_add100, mptest_echo,
    check_pickle, copy_via_pickle,
)
from .oop_tools import (
    # binding
    bind_to, Binding,
    # manage_attrs
    maintaining_attrs, using_attrs,
    maintain_attrs, use_attrs,
    MaintainingAttrs, UsingAttrs,
    UsingAttrsSignaled,
    IncrementableAttrManager,
    # oop_misc
    apply,
    MetaClsRepr,
)
from .os_tools import (
    InDir,
    with_dir,
    maintain_cwd, maintain_directory, maintain_dir,
    get_paths_with_common_start,
    next_unique_name,
    nbytes_path,
)
from .properties import (
    alias, alias_to_result_of, alias_child, alias_key_of, alias_in,
    weakref_property_simple,
    simple_property, simple_tuple_property,
    simple_setdefault_property, simple_setdefaultvia_property,
    elementwise_property,
    dict_with_defaults_property,
)
from .pytools import (
    format_docstring,
    printsource, displaysource,
    is_iterable,
    inputs_as_dict, _inputs_as_dict__maker,
    value_from_aliases,
    help_str, print_help_str, _help_str_paramdocs,
    indent_doclines, indent_paramdocs,
    pad_missing_format_keys, format_except_missing,
    replace_missing_format_keys, format_replace_missing,
)
from .sentinels import (
    Sentinel,
    UNSET, NO_VALUE, ATTR_UNSET, RESULT_MISSING,
)
from .supercomputer import (
    find_files_re, find_jobfiles, find_slurmfiles,
    slurm_nodes_from_slurmfile, n_slurm_nodes,
)
from .timing import (
    Profile,
    PROFILE, profiling, print_profile,
    Stopwatch, TickingWatch,
    ProgressUpdater,
    TimeLimit,
)
from .trees import Tree
from .xarray_accessors import (
    pcAccessor, pcArrayAccessor, pcDatasetAccessor,
)
from .xarrays import (
    is_iterable_dim,
    take_along_dimension, take_along_dimensions, join_along_dimension,
    xarray_differentiate,
    xarray_rename, xarray_assign, xarray_promote_dim, xarray_ensure_dims,
    nondim_coord_values, xarray_dims_coords, xarray_fill_coords,
    xarray_scale_coords, xarray_shift_coords,
    xarray_is_sorted,
    xarray_where_finite,
    xarray_get_dx_along,
    xarray_isel,
    xarray_map,
    # stats
    xarray_stats,
    # gaussian filter
    xarray_gaussian_filter,
    # coarsen / windowing
    xarray_coarsened,
    # polyfit
    xarray_polyfit, xarray_assign_polyfit_stddev, xarray_coarsened_polyfit,
)