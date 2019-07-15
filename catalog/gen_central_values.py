import numpy as np
import h5py as h5
from tqdm import tqdm



for i in tqdm(np.arange(0, 319)):
    f = h5.File('/Volumes/abeane_drive2/action_catalog/action_catalog_all_radv_pospar_'+str(i)+'.h5', 'r')
    actions, angles, freqs = f['actions'], f['angles'], f['freqs']
    this_med_actions = np.nanmedian(actions, axis=1)
    this_med_angles = np.nanmedian(angles, axis=1)
    this_med_freqs = np.nanmedian(freqs, axis=1)

    this_posvel = f['posvel']
    this_med_posvel = np.nanmedian(this_posvel, axis=1)

    this_actions_central = f['actions_central']
    this_angles_central = f['angles_central']
    this_freqs_central = f['freqs_central']

    this_source_id = f['source_id']

    if i==0:
        med_actions     = np.copy(this_med_actions)
        med_angles      = np.copy(this_med_angles)
        med_freqs       = np.copy(this_med_freqs)
        actions_central = np.copy(this_actions_central)

        actions_central = np.copy(this_actions_central) 
        angles_central  = np.copy(this_angles_central)
        freqs_central   = np.copy(this_freqs_central)

        source_id       = np.copy(this_source_id)
    else:
        med_actions     = np.concatenate((this_med_actions, med_actions))
        med_angles      = np.concatenate((this_med_angles, med_angles))
        med_freqs       = np.concatenate((this_med_freqs, med_freqs))
        actions_central = np.concatenate((this_actions_central, actions_central))
        actions_central = np.concatenate((this_actions_central, actions_central))
        angles_central  = np.concatenate((this_angles_central, angles_central))
        freqs_central   = np.concatenate((this_freqs_central, freqs_central))
        source_id       = np.concatenate((this_source_id, source_id))

    f.close()

fout = h5.File('central_action_catalog_all_radv_pospar'+'.h5', 'w')

fout.create_dataset('actions_median', data=med_actions)
fout.create_dataset('angles_median', data=med_angles)
fout.create_dataset('freqs_median', data=med_freqs)
fout.create_dataset('actions_central', data=actions_central)
fout.create_dataset('angles_central', data=angles_central)
fout.create_dataset('freqs_central', data=freqs_central)
fout.create_dataset('posvel_median', data=med_posvel)
fout.create_dataset('source_id', data=source_id, dtype='i8')

fout.close()
