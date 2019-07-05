import astropy.units as u
import numpy as np

import agama

import gala.potential as gp
import gala.dynamics as gd

# setup agama

agama.setUnits(mass=1, length=1, velocity=1)

# import the MW potential from gala
bulge = agama.Potential(type='Dehnen', gamma=1, mass=5E9, scaleRadius=1.0)           
nucleus = agama.Potential(type='Dehnen', gamma=1, mass=1.71E09, scaleRadius=0.07)   
disk = agama.Potential(type='MiyamotoNagai', mass=6.80e+10, scaleRadius=3.0, scaleHeight=0.28) 
halo = agama.Potential(type='NFW', mass=5.4E11, scaleRadius=15.62)                  
mwpot = agama.Potential(bulge, nucleus, disk, halo)

af = agama.ActionFinder(mwpot, interp=False)

pos_vel = np.array([8., 0., 0., 75., 150., 50.])
agama_act = af(pos_vel)

# now do it for gala

pot = gp.MilkyWayPotential()

w0 = gd.PhaseSpacePosition(pos=[8, 0, 0.]*u.kpc,
                           vel=[75, 150, 50.]*u.km/u.s)

w = gp.Hamiltonian(pot).integrate_orbit(w0, dt=0.5, n_steps=10000)
gala_act = gd.find_actions(w, N_max=8)
