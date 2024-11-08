"""
File Purpose: EbysusCollisionsLoader
"""

from ...errors import CollisionsModeError
from ...quantities import CollisionsLoader
from ...tools import UNSET, format_docstring

class EbysusCollisionsLoader(CollisionsLoader):
    '''collision frequency calculations.
    allows collisions_mode = 'helita' to get value via helita.
    '''
    @known_var(dims=['snap', 'fluid', 'jfluid'])
    def get_nusj_helita(self):
        '''collision frequency. (directly from Ebysus)
        for a single particle of s (self.fluid) to collide with any of j (self.jfluid).
        '''
        return self.load_maindims_var_across_dims('nu_ij', dims=['snap', 'fluid', 'jfluid'])

    COLLISIONS_MODE_OPTIONS = CollisionsLoader.COLLISIONS_MODE_OPTIONS.copy()
    COLLISIONS_MODE_OPTIONS['helita'] = \
            '''Use nusj_helita to get collision frequency.
            (However, for same fluid & jfluid, use 0 instead.)'''

    COLLISION_TYPE_TO_VAR = CollisionsLoader.COLLISION_TYPE_TO_VAR.copy()
    COLLISION_TYPE_TO_VAR['helita'] = 'nusj_helita'

    @format_docstring(docs_super=CollisionsLoader.collision_type)
    def collision_type(self, fluid=UNSET, jfluid=UNSET):
        '''Similar to super().collision_type, but return 'helita' if self.collisions_mode == 'helita'.
        (if fluid and jfluid are the same, return '0' instead.)
        
        super().collision_type docs copied here for reference:
        ----------------------------------------------------------
        {docs_super}
        '''
        try:
            return super().collision_type(fluid=fluid, jfluid=jfluid)
        except CollisionsModeError:
            if self.collisions_mode == 'helita':
                return 'helita'
            else:
                raise
