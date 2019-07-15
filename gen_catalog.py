import numpy as np
from pyia import GaiaData
from astropy.coordinates import Galactocentric
import astropy.units as u
from tqdm import tqdm
import h5py as h

import agama

agama.setUnits(mass=1, length=1, velocity=1)

# import the MW potential from gala
bulge = agama.Potential(type='Dehnen', gamma=1, mass=5E9, scaleRadius=1.0)
nucleus = agama.Potential(type='Dehnen', gamma=1, mass=1.71E09, scaleRadius=0.07)
disk = agama.Potential(type='MiyamotoNagai', mass=6.80e+10, scaleRadius=3.0, scaleHeight=0.28)
halo = agama.Potential(type='NFW', mass=5.4E11, scaleRadius=15.62)
mwpot = agama.Potential(bulge, nucleus, disk, halo)

af = agama.ActionFinder(mwpot, interp=False)

def convert_posvel_to_agama(g):
    x = g.x.to_value(u.kpc)
    y = g.y.to_value(u.kpc)
    z = g.z.to_value(u.kpc)
    vx = g.v_x.to_value(u.km/u.s)
    vy = g.v_y.to_value(u.km/u.s)
    vz = g.v_z.to_value(u.km/u.s)
    return np.transpose([x, y, z, vx, vy, vz])

def gen_act_cat(gaiadata, fout, nsamples=1024, seed=162,
                R0=8.175, sigmaR0=0.013, z0=20.8, sigmaz0=0.3,
                min_parallax=1e-3*u.mas):
    
    # generate the central galactocentric coordinate sytem
    galcen = Galactocentric(galcen_distance=R0*u.kpc, z_sun=z0*u.pc)

    # generate samples of the GC system
    # R0samples = np.random.normal(0, sigmaR0, nsamples)
    # z0samples = np.random.normal(0, sigmaz0, nsamples)

    # generate Monte Carlo samples of the observed coordinates
    g_samples = gaiadata.get_error_samples(size=nsamples, rnd=np.random.RandomState(seed=seed))

    g_galcen = gaiadata.skycoord.transform_to(galcen)

    # converting samples to galcen, some parallaxes will be negative due to sampling
    # even though the input catalog must have only positive parallaxes
    dist = g_samples.get_distance(min_parallax=min_parallax)
    c = g_samples.get_skycoord(distance=dist)
    g_samples_galcen = c.transform_to(galcen)

    samples_posvel = convert_posvel_to_agama(g_samples_galcen)
    samples_posvel_reshaped = np.reshape(samples_posvel, (len(gaiadata)*nsamples, 6))

    actions, angles, freqs = af(samples_posvel_reshaped, angles=True)

    actions[:,[1, 2]] = actions[:,[2, 1]]
    angles[:,[1, 2]] = angles[:,[2, 1]]
    freqs[:,[1, 2]] = freqs[:,[2, 1]]

    actions = np.reshape(actions, (nsamples, len(gaiadata), 3))
    angles = np.reshape(angles, (nsamples, len(gaiadata), 3))
    freqs = np.reshape(freqs, (nsamples, len(gaiadata), 3))

    actions = np.swapaxes(actions, 0, 1)
    angles = np.swapaxes(angles, 0, 1)
    freqs = np.swapaxes(freqs, 0, 1)
    samples_posvel = np.swapaxes(samples_posvel, 0, 1)

    posvel_central = convert_posvel_to_agama(g_galcen)
    actions_c, angles_c, freqs_c = af(posvel_central, angles=True)

    actions_c[:,[1, 2]] = actions_c[:,[2, 1]]
    angles_c[:,[1, 2]] = angles_c[:,[2, 1]]
    freqs_c[:,[1, 2]] = freqs_c[:,[2, 1]]

    with h.File(fout, 'w') as f:
        f.create_dataset('actions', data=actions)
        f.create_dataset('angles', data=angles)
        f.create_dataset('freqs', data=freqs)
        f.create_dataset('posvel', data=samples_posvel)

        f.create_dataset('actions_central', data=actions_c)
        f.create_dataset('angles_central', data=angles_c)
        f.create_dataset('freqs_central', data=freqs_c)

        f.create_dataset('source_id', data=gaiadata.source_id, dtype='i8')

    return None

if __name__ == '__main__':
    g = GaiaData('data/gaiadr2_top100_100pc.fits')
    gen_act_cat(g, 'catalog/action_catalog.h5', nsamples=256)
