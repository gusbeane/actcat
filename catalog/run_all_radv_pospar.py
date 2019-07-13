import sys
sys.path.append('../')

from gen_catalog import gen_act_cat
from pyia import GaiaData
import numpy as np

chunk=20000
nsamples=256

g = GaiaData('../data/gaiadr2_all_radv.fits')
k = np.where(g.parallax.value > 0)[0]

dividers = np.arange(0, len(k), chunk)
for i in range(len(dividers)-1):
    gen_act_cat(g[k][dividers[i]:dividers[i+1]], '/Volumes/abeane_drive2/action_catalog/action_catalog_all_radv_pospar_'+str(i)+'.h5', nsamples=nsamples)
gen_act_cat(g[k][dividers[-1]:], '/Volumes/abeane_drive2/action_catalog/action_catalog_all_radv_pospar_'+str(len(dividers)-1)+'.h5', nsamples=nsamples)
