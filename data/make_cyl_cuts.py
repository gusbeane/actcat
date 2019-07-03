import numpy as np
from pyia import GaiaData
import astropy.units as u
from astropy.coordinates import Galactocentric
from astropy.table import Table

Rcut = 250 * u.pc
zcut = 2 * u.kpc

gmag_max = 6.5
gmag_min = 3.2
bprp_min = 0.5
bprp_max = 1.2

R0=8.175 * u.kpc
z0=20.8 * u.pc
galcen = Galactocentric(galcen_distance=R0, z_sun=z0)

g = GaiaData('gdr2_radv_actions_noerrors.fits')

coord = g.skycoord.transform_to(galcen)

R = np.sqrt(np.square(coord.x + R0) + np.square(coord.y))
z = np.abs(coord.z)

bool1 = R < Rcut
bool2 = z < zcut

xybool = np.logical_and(bool1, bool2)

gapp = g.phot_g_mean_mag.value 
dist = g.distance.to_value(u.pc)
gmag = gapp - 5 * (np.log10(dist)-1)
bprp = g.bp_rp.value

gbool = np.logical_and(gmag > gmag_min, gmag < gmag_max)
bprpbool = np.logical_and(bprp > bprp_min, bprp < bprp_max)
magbool = np.logical_and(gbool, bprpbool)

totbool = np.logical_and(xybool, magbool)
keys = np.where(totbool)[0]

t = Table.read('gdr2_radv_actions_noerrors.fits', format='fits')
t_write = t[keys]
t_write.write('gdr2_radv2_cylcut_bandcut.fits', format='fits')
