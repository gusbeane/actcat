from gen_catalog import gen_act_cat
from pyia import GaiaData

g = GaiaData('../data/gdr2_radv2_cylcut_bandcut.fits')
gen_act_cat(g, 'action_catalog_cylcut_bandcut.pickle')
