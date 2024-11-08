"""
File Purpose: calculating plasma drifts, e.g. hall, pederson.
"""
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

from .plasma_parameters import PlasmaParametersLoader
from ..plotting import PlotSettings


class PlasmaDriftsLoader(PlasmaParametersLoader):
    '''plasma drifts.'''
    # # # GET DRIFTS # # #
    @known_var(deps=['skappa', 'E_cross_B', 'mod_B'])
    def get_u_hall(self, *, _E=None, _B=None):
        '''Hall drift velocity. u_hall = (kappa**2 / (1 + kappa**2)) * (E x B) / |B|**2,
        where kappa is the magnetization parameter, kappa = gyrof / nusn.
        [EFF] for efficiency, can provide E and/or B, if already known.
        '''
        skappa = self('skappa')  # signed kappa; skappa<0 when q<0.
        E_cross_B = self('E_cross_B', _E=_E, _B=_B)
        mod_B = self('mod_B', _B=_B)
        return ((skappa**2 / (1 + skappa**2)) / mod_B**2) * E_cross_B 

    @known_var(deps=['skappa', 'E', 'mod_B'], aliases=['u_ped'])
    def get_u_pederson(self, *, _E=None, _B=None):
        '''Pederson drift velocity. u_pederson = (skappa / (1 + skappa**2)) * E / |B|,
        where skappa is the (signed) magnetization parameter, skappa = q * |B| / (m * nusn).
        [EFF] for efficiency, can provide E and/or B, if already known.
        '''
        skappa = self('skappa')  # signed kappa; skappa<0 when q<0.
        E = self('E') if _E is None else _E
        mod_B = self('mod_B', _B=_B)
        return ((skappa / (1 + skappa**2)) / mod_B) * E 

    @known_var(deps=['skappa', 'E_dot_B', 'B', 'mod_B'])
    def get_u_EdotB(self, *, _E=None, _B=None):
        '''EdotB drift velocity. u_EdotB = (skappa**3 / (1 + skappa**2)) * (E dot B) B / |B|^3
        (Commonly neglected, but comes from the same physical equation as hall & pederson drifts;
        from solving equilibrium momentum equation for u, when neglecting all derivatives.)
        [EFF] for efficiency, can provide E and/or B, if already known.
        '''
        skappa = self('skappa')
        E_dot_B = self('E_dot_B', _E=_E, _B=_B)
        B = self('B') if _B is None else _B
        mod_B = self('mod_B', _B=_B)
        return ((skappa**3 / (1 + skappa**2)) * B / mod_B**3) * E_dot_B

    @known_var(deps=['u_hall', 'u_pederson', 'u_EdotB'], aliases=['u_eqcol', 'eqcol_u'])
    def get_u_drift(self):
        '''equilibrium velocity; solution to the momentum equation with collisions,
        assuming zero acceleration and zero spatial gradients.
        u_drift = u_hall + u_pederson + u_EdotB.
        '''
        # [EFF] calculate E & B first, to avoid recalculating them 3 times.
        #   will need all components of E & B, even if len(self.component)==1,
        #   because internally will calculate E cross B AND E dot B.
        with self.using(component=None):  # all components
            E = self('E')
            B = self('B')
        return self('u_hall', _E=E, _B=B) + self('u_pederson', _E=E, _B=B) + self('u_EdotB', _E=E, _B=B)
        # inefficient way: recalculates E & B, each time:
        # return self('u_hall') + self('u_pederson') + self('u_EdotB')

    # # # GET KAPPA & NUSN FROM VELOCITIES (assuming velocities are from drifts) # # #
    # note - example plotting code for these quantities can be found in eppic_moments.py

    @known_pattern(r'skappa_from_(means_|)(.*_)?momExB', ignores_dims=['component'],
                   deps=[lambda ql, var, groups: 'u' if groups[1] is None else groups[1][:-len('_')],
                        'u_neutral', 'u_cross_B', 'mod_B', 'E_cross_B',])
    def get_skappa_from_momExB(self, var, *, _match=None):
        '''signed kappa (magnetization parameter) that statisfies momentum equation in the E x B direction.
        'skappa_from_{means_}{u_}momExB'
            E.g. 'skappa_from_means_momExB', 'skappa_from_momExB', 'skappa_from_means_moment1_momExB'
            {means_} = 'means_' or ''.
                if 'means_', take means of vars: 'u', 'u_neutral', 'mod_B', 'E_cross_B', 'u_cross_B'
            {u_} = '' or any other var then '_'.
                if provided, use this var instead of 'u' for velocity.  (Doesn't affect "u_neutral" though.)
                E.g. eppic calculator might use 'moment1' here, as in 'skappa_from_moment1_momExB'.

        Algebraic solution:
            momentum equation, rearranged using skappa = q * |B| / (m * nusn):
                0 = q (E + u x B) - m * nusn * (u - u_neutral)
                0 = skappa (E + u x B) - |B| (u - u_neutral)
            dotting with E x B:
                0 = skappa [(u x B) dot (E x B)] - |B| [(u - u_neutral) dot (E x B)]
                --> skappa = |B| [(u - u_neutral) dot (E x B)] / [(u x B) dot (E x B)]
        '''
        # Note, the denominator can be "simplified" further (but is not in this method) via:
        # (u x B) dot (E x B) = (u dot B) (E dot B) - (u dot E) |B|^2
        means, uvar = _match.groups()
        mean = 'mean_' if means else ''   # default ''
        ustr = uvar[:-len('_')] if uvar else 'u'
        with self.using(component=None):  # make sure to get all components of vectors.
            u = self(f'{mean}{ustr}')
            u_n = self(f'{mean}u_neutral')
            mod_B = self(f'{mean}mod_B')
            E_cross_B = self(f'{mean}E_cross_B')
            u_cross_B = self(f'{mean}{ustr}_cross_B')
            skappa = mod_B * self.dot(u - u_n, E_cross_B) / self.dot(u_cross_B, E_cross_B)
        return skappa

    @known_pattern(r'skappa_from_(means_|)(.*_)?momE', ignores_dims=['component'],
                   deps=[lambda ql, var, groups: 'u' if groups[1] is None else groups[1][:-len('_')],
                        'u_neutral', 'E', 'mod_B', 'E_cross_B',])
    def get_skappa_from_momE(self, var, *, _match=None):
        '''signed kappa (magnetization parameter) that statisfies momentum equation in the E direction.
        'skappa_from_{means_}{u_}momE'
            E.g. 'skappa_from_means_momE', 'skappa_from_momE', 'skappa_from_means_moment1_momE'
            {means_} = 'means_' or ''.
                if 'means_', take means of vars: 'u', 'u_neutral', 'mod_E', 'mod_B', 'E', 'E_cross_B'
            {u_} = '' or any other var then '_'.
                if provided, use this var instead of 'u' for velocity.  (Doesn't affect "u_neutral" though.)
                E.g. eppic calculator might use 'moment1' here, as in 'skappa_from_moment1_momE'.

        Algebraic solution:
            momentum equation, rearranged using skappa = q * |B| / (m * nusn):
                0 = q (E + u x B) - m * nusn * (u - u_neutral)
                0 = skappa (E + u x B) - |B| (u - u_neutral)
            dotting with E:
                0 = skappa (|E|^2 + (u x B) dot E) - |B| (u - u_neutral) dot E    # note uxB.E == BxE.u == -ExB.u
                --> skappa = |B| (u - u_neutral) dot E / (|E|^2 - u dot (E x B))

        Note: results untrustworthy when kappa >> 1, since that involves dividing by a value close to 0.
        '''
        means, uvar = _match.groups()
        mean = 'mean_' if means else ''
        ustr = uvar[:-len('_')] if uvar else 'u'
        with self.using(component=None):  # make sure to get all components of vectors.
            u = self(f'{mean}{ustr}')
            u_n = self(f'{mean}u_neutral')
            E = self(f'{mean}E')
            mod_B = self(f'{mean}mod_B')
            E_cross_B = self(f'{mean}E_cross_B')
            mod_E_squared = self('mean_mod_E')**2 if means else self.dot(E,E)  # [EFF] use known E if not taking means.
            skappa = mod_B * self.dot(u - u_n, E) / (mod_E_squared - self.dot(u, E_cross_B))
        return skappa

    # [TODO] skappa from momB which gets skappa that satisfies momentum equation in the B direction.
    # (it is undetermined when E dot B == 0 == u dot B, so it's not useful if B perp to 2D simulation plane.)

    @known_pattern(r'skappa_from_(means_|)(.*_)?hall', ignores_dims=['component'],
                   deps=[lambda ql, var, groups: 'u' if groups[1] is None else groups[1][:-len('_')],
                        'mod_B', 'E_cross_B', 'q'])
    def get_skappa_from_hall(self, var, *, _match=None):
        '''signed kappa (magnetization parameter) that statisfies u_hall = u, in the E x B direction.
        'skappa_from_{means_}{u_}hall'
            E.g. 'skappa_from_means_hall', 'skappa_from_hall', 'skappa_from_means_moment1_hall'
            {means_} = 'means_' or ''.
                if 'means_', take means of vars: 'u', 'u_neutral', 'mod_B', 'E_cross_B'
            {u_} = '' or any other var then '_'.
                if provided, use this var instead of 'u' for velocity.  (Doesn't affect "u_neutral" though.)
                E.g. eppic calculator might use 'moment1' here, as in 'skappa_from_moment1_hall'.

        Algebraic solution:
            formula for u_hall (from solving momentum equation for u in the E x B direction):
                u_hall = (kappa**2 / (1 + kappa**2)) * (E x B) / |B|**2
            solving for kappa**2, assuming u instead of u_hall, yields:
                (u dot (E x B)) == (kappa**2 / (1 + kappa**2)) * (|E x B|**2 / |B|**2)
                A + A * kappa**2 - kappa**2 == 0, where A = (u dot (E x B)) / (|E x B|**2 / |B|**2)
                kappa**2 = A / (1 - A)
                --> skappa = +- sqrt(A / (1 - A)),
            There are two solutions; return solution with the same sign as self('q') (i.e. fluid's charge)
        '''
        means, uvar = _match.groups()
        mean = 'mean_' if means else ''
        ustr = uvar[:-len('_')] if uvar else 'u'
        u_n = self(f'{mean}u_neutral')
        if np.any(u_n != 0):  # [TODO] account for nonzero u_neutral in this method.
            raise NotImplementedError(f'{var!r} when u_neutral != 0.')
        with self.using(component=None):  # make sure to get all components of vectors.
            u = self(f'{mean}{ustr}')
            mod_B = self(f'{mean}mod_B')
            E_cross_B = self(f'{mean}E_cross_B')
            A = self.dot(u, E_cross_B) / (self.dot(E_cross_B, E_cross_B) / mod_B**2)
            sign = np.sign(self('q'))
            skappa = sign * (A / (1 - A))**0.5
        return skappa

    @known_pattern(r'skappa_from_(means_|)(.*_)?pederson', ignores_dims=['component'],
                   deps=[lambda ql, var, groups: 'u' if groups[1] is None else groups[1][:-len('_')],
                        'u_neutral', 'mod_B', 'E', 'q'])
    def get_skappa_from_pederson(self, var, *, _match=None):
        '''signed kappa (magnetization parameter) that statisfies u_pederson = u, in the E direction.
        'skappa_from_{means_}{u_}pederson'
            E.g. 'skappa_from_means_pederson', 'skappa_from_pederson', 'skappa_from_means_moment1_pederson'
            {means_} = 'means_' or ''.
                if 'means_', take means of vars: 'u', 'u_neutral', 'mod_B', 'E', 'mod_E',
            {u_} = '' or any other var then '_'.
                if provided, use this var instead of 'u' for velocity.  (Doesn't affect "u_neutral" though.)
                E.g. eppic calculator might use 'moment1' here, as in 'skappa_from_moment1_pederson'.

        Algebraic solution:
            formula for u_pederson (from solving momentum equation for u in the E direction):
                u_pederson = (skappa / (1 + skappa**2)) * E / |B|
            solving for skappa, assuming u instead of u_pederson, yields:
                (u dot E) == (skappa / (1 + skappa**2)) * (|E|**2 / |B|)
                A + A * skappa**2 - skappa == 0, where A = (u dot E) / (|E|**2 / |B|)
                skappa = (1 +- sqrt((-1)^2 - 4 * A * A)) / (2 * A),
            There are two solutions; the correct choice can be determined by using the momentum equation;
                the correct choice for the +- sign turns out to be: -sign(q) where q = self('q') == fluid's charge.

        Note: results untrustworthy when kappa >> 1, since that involves dividing by a value close to 0.
        '''
        means, uvar = _match.groups()
        mean = 'mean_' if means else ''
        ustr = uvar[:-len('_')] if uvar else 'u'
        u_n = self(f'{mean}u_neutral')
        if np.any(u_n != 0):  # [TODO] account for nonzero u_neutral in this method.
            raise NotImplementedError(f'{var!r} when u_neutral != 0.')
        with self.using(component=None):  # make sure to get all components of vectors.
            u = self(f'{mean}{ustr}')
            mod_B = self(f'{mean}mod_B')
            E = self(f'{mean}E')
            mod_E_squared = self('mean_mod_E')**2 if means else self.dot(E,E)  # [EFF] use known E if not taking means.
            A = self.dot(u, E) / (mod_E_squared / mod_B)
            qsign = np.sign(self('q'))
            skappa = (1 - qsign * (1 - 4 * A**2)**0.5) / (2 * A)
        return skappa

    @known_pattern(r'nusn_from_(means_|)(.*_)?(momExB|momE|hall|pederson)', ignores_dims=['component'],
                   deps=['sgyrof', lambda ql, var, groups: 'skappa'+var[len('nusn'):]])
    def get_nusn_from_drift(self, var, *, _match=None):
        '''nusn, calculated by assuming u satisfies momentum equation to zeroth order.
        There are various options for how to solve for nusn, as explained below (see {drift}).
        All solutions use nusn = sgyrof / skappa, where skappa is determined via
            skappa = self('skappa'+var[len('nusn'):]).
        E.g. 'nusn_from_means_momExB' --> use skappa = self('skappa_from_means_momExB').

        The description below helps explain the various options.

        'nusn_from_{means_}{u_}{drift}'
            E.g. 'nusn_from_means_momExB', 'nusn_from_hall', 'nusn_from_means_moment1_momB'
            {means_} = 'means_' or ''.
                if 'means_', take means of vars: 'sgyrof', any vars relevant to the chosen {drift} option.
            {u_} = '' or any other var then '_'.
                if provided, use this var instead of 'u' for velocity.  (Doesn't affect "u_neutral" though.)
            {drift} = 'momExB', 'momE', 'hall', or 'pederson'
                indicates how to solve for nusn. Use the similarly-named var when getting skappa.
                'momExB' --> get skappa from the momentum equation in the E x B direction.
                'momE' --> get skappa from the momentum equation in the E direction.
                'hall' --> get skappa from u_hall = u, in the E x B direction.
                'pederson' --> get skappa from u_pederson = u, in the E direction.
        '''
        means, uvar, drift = _match.groups()
        if uvar is None: uvar = ''
        kvar = f'skappa_from_{means}{uvar}{drift}'
        skappa = self(kvar)
        return self('sgyrof') / skappa

    def plot_check_nusn_from_drift(self, *, u='u', drift='momExB', cycle1=dict(ls=['-', '--', '-.', ':']),
                                   means=True, log=True, **kw_timelines):
        '''plots PlasmaCalcs.timelines() for comparing nusn to nusn inferred from drifts.
        This is meant to be used as a quick check. Use this code as an example if you need more low-level control.

        u: str or iterable of strs
            var to use for velocity. Might want something else, e.g. EppicCalculator might use u='moment1'
            iterable of strs --> get multiple.
        drift: str or iterable of strs
            tells the way to infer skappa, and thus nusn. Options: 'momExB', 'momE', 'hall', 'pederson'.
            iterable of strs --> get multiple.
        cycle1: dict of lists
            parameters to use for matplotlib plotting if getting multiple u or drift.
        means: bool
            whether to take means of lower-level vars while getting skappa.
            (e.g. use 'skappa_from_means_momExB' instead of 'skappa_from_momExB', if True.)
        log: bool
            whether to take log10 of the ratios (nusn_from_drift / nusn) before plotting.

        returns plt.gcf().
        '''
        mean = 'means_' if means else ''
        log10 = 'log10_' if log else ''
        if isinstance(u, str):
            u = [u]
        if isinstance(drift, str):
            drift = [drift]
        Nlines = len(u) * len(drift)
        Lcycle = None if len(cycle1)==0 else min(len(val) for val in cycle1.values())
        if (Lcycle is not None) and (Nlines > Lcycle):
            print(f'warning, too many timelines ({Nlines}) compared to style cycle length ({Lcycle}).')
        kw_timelines['ybounds'] = kw_timelines.pop('ybounds', PlotSettings.get_default('ybounds'))
        i = 0
        for uvar in u:
            for driftvar in drift:
                # calculation
                arr = self(f'{log10}(mean_(nusn_from_{mean}{uvar}_{driftvar}/nusn))')
                # plotting
                style = {k: v[i] for k,v in cycle1.items()}
                tls = arr.pc.timelines(label=f'({uvar}_{driftvar})', **style, **kw_timelines)
                # bookkeeping
                kw_timelines['ybounds'] = plt.ylim()  # ensure later timelines' ylims are big enough to show all timelines.
                i += 1
        # plot formatting
        plt.ylabel(f'{log10}(nusn_from_drift / nusn)')
        plt.title('check nusn from drift' if getattr(self, 'title', None) is None else self.title)

        return plt.gcf()
