import numpy as np
import h5py as h5
from tqdm import tqdm

for i in tqdm(np.arange(0, 319)):
    f = h5.File('/Volumes/abeane_drive2/action_catalog/action_catalog_all_radv_pospar_'+str(i)+'.h5', 'r')
    actions, angles, freqs = f['actions'], f['angles'], f['freqs']
    med_actions = np.nanmedian(actions, axis=1)
    med_angles = np.nanmedian(angles, axis=1)
    med_freqs = np.nanmedian(freqs, axis=1)

    posvel = f['posvel']
    med_posvel = np.nanmedian(posvel, axis=1)

    fout = h5.File('central_action_catalog_all_radv_pospar_'+str(i)+'.h5', 'w')

    fout.create_dataset('actions_median', data=med_actions)
    fout.create_dataset('angles_median', data=med_angles)
    fout.create_dataset('freqs_median', data=med_freqs)

    fout.create_dataset('actions_central', data=f['actions_central'])
    fout.create_dataset('angles_central', data=f['angles_central'])
    fout.create_dataset('freqs_central', data=f['freqs_central'])

    fout.create_dataset('posvel_median', data=med_posvel)

    fout.create_dataset('source_id', data=f['source_id'])

    f.close()
    fout.close()
