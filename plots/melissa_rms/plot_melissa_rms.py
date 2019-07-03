import matplotlib.pyplot as plt
from pyia import GaiaData
import numpy as np
import h5py as h
from tqdm import tqdm

f = h.File('../../catalog/action_catalog_cylcut_bandcut.h5', 'r')
g = GaiaData('../../data/gdr2_radv2_cylcut_bandcut.fits')

keys = list(f.keys())

med_data = np.array([np.nanmedian(f[k], axis=0) for k in tqdm(keys)])
std_data = np.array([np.nanstd(f[k], axis=0, ddof=1) for k in tqdm(keys)])

rms = (g.parallax_over_error**2 + (g.radial_velocity/g.radial_velocity_error)**2 + (g.pmra/g.pmra_error)**2 + (g.pmdec/g.pmdec_error)**2)**(0.5)
rms_n = (g.parallax_over_error**(-2) + (g.radial_velocity/g.radial_velocity_error)**(-2) + (g.pmra/g.pmra_error)**(-2) + (g.pmdec/g.pmdec_error)**(-2))**(-0.5)

rms_act = ((med_data[:,0]/std_data[:,0])**2 + (med_data[:,1]/std_data[:,1])**2 + (med_data[:,2]/std_data[:,2])**2)**(0.5)
rms_act_n = ((med_data[:,0]/std_data[:,0])**(-2) + (med_data[:,1]/std_data[:,1])**(-2) + (med_data[:,2]/std_data[:,2])**(-2))**(-0.5)

Jzbool = med_data[:,2] < 10
Jkeys = np.where(Jzbool)[0]

plt.scatter(rms_act[Jkeys], rms[Jkeys], s=0.1)
plt.plot([0, 2000], [0, 2000])
plt.xlim(0, 1000)
plt.ylim(0, 2000)
plt.savefig('rms.png')
plt.close()

plt.scatter(rms_act_n[Jkeys], rms_n[Jkeys], s=0.1)
plt.plot([0, 500], [0, 500])
plt.xlim(0, 250)
plt.ylim(0, 250)
plt.savefig('rms_n.png')
