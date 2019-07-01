import numpy as np
from pyia import GaiaData
from astropy.coordinates import Galactocentric
from astropy.coordinates import CylindricalRepresentation, CylindricalDifferential
import astropy.units as u

from galpy.potential import MWPotential2014, vcirc
from galpy.actionAngle import estimateDeltaStaeckel, actionAngleStaeckel
from galpy.orbit import Orbit

def convert_to_galpy(g, R0, v0):
    R = g.rho
    z = g.z
    vR = g.differentials['s'].d_rho
    vT = g.differentials['s'].d_phi * R
    vT = vT.to(u.km/u.s, equivalencies=u.dimensionless_angles())
    vz = g.differentials['s'].d_z
    return R.to_value(u.kpc)/R0, vR.to_value(u.km/u.s)/v0, vT.to_value(u.km/u.s)/v0, z.to_value(u.kpc)/R0, vz.to_value(u.km/u.s)/v0

galcen = Galactocentric()
R0 = 8
v0 = 220

g = GaiaData('data/gaiadr2_top100_100pc.fits')
g_samples = g.get_error_samples(size=1024, rnd=np.random.RandomState(seed=162))

g_galcen = g.skycoord.transform_to(galcen)
g_samples_galcen = g_samples.skycoord.transform_to(galcen)

g_galcen_cyl = g_galcen.represent_as(CylindricalRepresentation, CylindricalDifferential)
g_samples_galcen_cyl = g_samples_galcen.represent_as(CylindricalRepresentation, CylindricalDifferential)

