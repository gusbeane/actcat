import numpy as np
from pyia import GaiaData
from astropy.coordinates import Galactocentric
import astropy.units as u

import agama

agama.setUnits(mass=1, length=1, velocity=1)

# import the MW potential from gala
bulge = agama.Potential(type='Dehnen', gamma=1, mass=5E9, a=1.0)           
nucleus = agama.Potential(type='Dehnen', gamma=1, mass=1.71e+09, a=0.07)   
disk = agama.Potential(type='MiyamotoNagai', mass=6.80e+10, a=3.0, b=0.28) 
halo = agama.Potential(type='NFW', mass=5.4E11, a=15.62)                  
mwpot = agama.Potential(bulge, nucleus, disk, halo)

af = agama.ActionFinder(mwpot, interp=False)

def convert_to_agama(g):
    x = g.x.to_value(u.kpc)
    y = g.y.to_value(u.kpc)
    z = g.z.to_value(u.kpc)
    vx = g.v_x.to_value(u.km/u.s)
    vy = g.v_y.to_value(u.km/u.s)
    vz = g.v_z.to_value(u.km/u.s)
    return np.transpose([x, y, z, vx, vy, vz])

galcen = Galactocentric()

g = GaiaData('data/gaiadr2_top100_100pc.fits')
g_samples = g.get_error_samples(size=1024, rnd=np.random.RandomState(seed=162))

g_galcen = g.skycoord.transform_to(galcen)
g_samples_galcen = g_samples.skycoord.transform_to(galcen)

for central, samples in zip([g_galcen[0]], [g_samples_galcen[0]]):
    pos_vel = convert_to_agama(samples)
    actions, angles, freqs = af(pos_vel, angles=True)
    actions[:,[1, 2]] = actions[:,[2, 1]]
    angles[:,[1, 2]] = angles[:,[2, 1]]
    freqs[:,[1, 2]] = freqs[:,[2, 1]]
