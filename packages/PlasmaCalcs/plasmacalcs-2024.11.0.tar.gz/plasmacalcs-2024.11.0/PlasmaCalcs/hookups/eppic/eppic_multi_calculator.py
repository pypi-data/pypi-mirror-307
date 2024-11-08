"""
File Purpose: EppicMultiCalculator
(multiple EppicCalculators across multiple Eppic runs)
"""
# import os

# from .eppic_calculator import EppicCalculator
# from .eppic_dimensions import EppicRunList
# from ...multi_run_analysis import MultiCalculator, _paramdocs_multicalculator
# from ...tools import (
#     format_docstring,
# )

# def _eppic_calculator_from_path(path, **kw_init):
#     '''return an EppicCalculator from the given path.
#     Users should prefer to use EppicCalculator.from_here() instead;
#         this method is intended as a helper method for EppicMultiCalculator.
#     '''
#     file = os.path.join(path, 'eppic.i')
#     return EppicCalculator.from_here(file, **kw_init)


# @format_docstring(**_paramdocs_multicalculator)
# class EppicMultiCalculator(MultiCalculator):  # [TODO] inherit from EppicCalculator too?
#     '''A MultiCalculator for EppicCalculators.
#     tracks & uses a list of PlasmaCalculator objects when getting values.
#     Each PlasmaCalculator will be associated with a Run value in the results.

#     CAUTION: initializing this class WILL AFFECT the individual calculators!
#         in particular, for each c in calculators, it may adjust:
#             c.extra_coords, c.snaps, c.snap.

#     runs: {runs}
#     join: {join}
#     ncpu: {ncpu}
#     '''
#     run_list_cls = EppicRunList  # use this class when creating runs in classmethods e.g. from_here
#     calculator_maker = _eppic_calculator_from_path  # callable of path -> EppicCalculator

#     # most functionality is inherited from MultiCalculator.
