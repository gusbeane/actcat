from pyia import GaiaData
import astropy.units as u
import h5py as h5
import numpy as np

g = GaiaData('../data/gaiadr2_all_radv.fits')
f = h5.File('central_action_catalog_all_radv_pospar.h5')

for dcut in [200*u.pc, 600*u.pc]:
    dist = g.get_distance()
    keys = np.where(dist < dcut)[0]
    sids = g.source_id[keys]

    fkeys = np.where(np.isin(f['source_id'], sids))[0]

    fout = h5.File('central_action_catalog_all_radv_pospar_'+str(dcut.to_value(u.pc))+'pc.h5', 'w')
    for k in list(f.keys()):
        fout.create_dataset(k, data=f[k][fkeys], dtype=f[k].dtype)
    fout.close()
f.close()
