"""
File Purpose: MultiCalculator
"""

from ..tools import (
    DictOfSimilar,
)

class MultiCalculator(DictOfSimilar):
    '''a class to handle multiple calculators.

    Example:
        calc1 = PlasmaCalculator(...)
        calc2 = PlasmaCalculator(...)
        mc = MultiCalculator({'c1':calc1, 'c2':calc2})
        mc.snap = 0             # sets calc.snap=0 for all calcs
        mc['slices', 'x'] = 7   # sets calc.slices['x'] = 7 for all calcs
        mc('Eheat')             # returns list of calc('Eheat') for all calcs
    '''
    cls_new = DictOfSimilar  # results will be DictOfSimilar instead of MultiCalculator.

    def _get_similar_attrs(self):
        '''return SIMILAR ATTRS for self.
        This is the intersection of all kw_call_options from calculators in self.
        '''
        # [EFF] if this ever becomes slow, use caching.
        options = [set(calc.kw_call_options()) for calc in self.values()]
        return set.intersection(*options)

    SIMILAR_ATTRS = property(lambda self: self._get_similar_attrs(),
        doc='''SIMILAR_ATTRS for self; operations on self will be broadcasted to these attrs,
        e.g. self.snap = 0 --> [calc.snap for calc in self.values()], if 'snap' in SIMILAR_ATTRS.''')

    @property
    def title(self):
        '''return a title for self: f'{calc1.title}|{calc2.title}|...|{calcN.title}'.'''
        return '|'.join([calc.title for calc in self.values()])
