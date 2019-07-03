from gen_catalog import gen_act_cat
from pyia import GaiaData
import numpy as np

g = GaiaData('../data/gdr2_radv2_cylcut_bandcut.fits')
k = np.where(g.parallax.value > 0)[0]
gen_act_cat(g[k][:100000], 'action_catalog_cylcut_bandcut.h5')
