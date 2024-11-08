"""
File Purpose: MultiDimensionHaver

It sets the dimension for all calculators.
E.g. obj.snap = 4 --> setattr(c, 'snap', 4) for c in obj.calculators
"""
from ..dimensions import DimensionHaver
from ..errors import SnapValueError, FluidValueError, ComponentValueError

class MultiDimensionHaver(DimensionHaver):
    def __init__(self):
        raise NotImplementedError('[TODO] - this class...')

    @property
    def snaps(self):
        '''snaps; must be the same object in c.snaps for all c in self.calculators.
        raise SnapValueError if not all calculators have the same snaps.
        '''
        snaps = self.calculators[0].snaps
        for c in self.calculators[1:]:
            if c.snaps != snaps:
                raise SnapValueError('not all calculators have the same snaps.')
        return snaps

    @property
    def snap(self):
        '''snap; setting self.snap=v will set c.snap=v for all c in self.calculators.
        getting self.snap will return the unambiguous "current snap", i.e. c.snap,
            but raise SnapValueError if not all calculators have the same snap.
        '''
        snap = self.calculators[0].snap
        for c in self.calculators[1:]:
            if c.snap != snap:
                raise SnapValueError('not all calculators have the same snap.')
        return snap
    @snap.setter
    def snap(self, v):
        for c in self.calculators:
            c.snap = v

    @property
    def fluids(self):
        '''fluids; must be the same object in c.fluids for all c in self.calculators.
        raise FluidValueError if not all calculators have the same fluids.
        '''
        fluids = self.calculators[0].fluids
        for c in self.calculators[1:]:
            if c.fluids != fluids:
                raise FluidValueError('not all calculators have the same fluids.')
        return fluids

    @property
    def fluid(self):
        '''fluid; setting self.fluid=v will set c.fluid=v for all c in self.calculators.
        getting self.fluid will return the unambiguous "current fluid", i.e. c.fluid,
            but raise SnapValueError if not all calculators have the same fluid.
        '''
        fluid = self.calculators[0].fluid
        for c in self.calculators[1:]:
            if c.fluid != fluid:
                raise FluidValueError('not all calculators have the same fluid.')
        return fluid
    @fluid.setter
    def fluid(self, v):
        for c in self.calculators:
            c.fluid = v