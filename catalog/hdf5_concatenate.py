import numpy as np
import h5py as h5
from tqdm import tqdm

def hdf5_concatenate(file_list, file_out):
    f0 = h5.File(file_list[0], 'r')

    key_list = list(f0.keys())

    shape_dict = {}
    for i,file in enumerate(file_list):
        f = h5.File(file, 'r')
        for key in key_list:
            if i==0:
                shape_dict[key] = list(np.shape(f[key]))
            else:
                shape_dict[key][0] += np.shape(f[key])[0]
        f.close()

    fout = h5.File(file_out, 'w')
    ctr_dict = {}
    for key in key_list:
        fout.create_dataset(key, shape_dict[key])
        ctr_dict[key] = 0

    for i,file in enumerate(tqdm(file_list)):
        f = h5.File(file, 'r')
        for key in key_list:
            sz = np.shape(f[key])[0]
            fout[key][ctr_dict[key]:ctr_dict[key]+sz] = f[key]
            ctr_dict[key] += sz
    fout.close()

if __name__ == '__main__':
    file_list = ['central_action_catalog_all_radv_pospar_'+str(i)+'.h5' for i in range(319)]
    hdf5_concatenate(file_list, 'central_action_catalog_all_radv_pospar.h5')


# for i in tqdm(np.arange(0, 319)):
#     f = h5.File('central_action_catalog_all_radv_pospar_'+str(i)+'.h5', 'r')

#     this_med_actions = f['actions_median']
#     this_med_angles = f['angles_median']
#     this_med_freqs = f['freqs_median']

#     this_med_posvel = f['posvel_median']

#     this_actions_central = f['actions_central']
#     this_angles_central = f['angles_central']
#     this_freqs_central = f['freqs_central']

#     this_source_id = f['source_id']

#     if i==0:
#         med_actions     = np.copy(this_med_actions)
#         med_angles      = np.copy(this_med_angles)
#         med_freqs       = np.copy(this_med_freqs)
#         actions_central = np.copy(this_actions_central)

#         actions_central = np.copy(this_actions_central) 
#         angles_central  = np.copy(this_angles_central)
#         freqs_central   = np.copy(this_freqs_central)

#         source_id       = np.copy(this_source_id)
#     else:
#         med_actions     = np.concatenate((this_med_actions, med_actions))
#         med_angles      = np.concatenate((this_med_angles, med_angles))
#         med_freqs       = np.concatenate((this_med_freqs, med_freqs))
#         actions_central = np.concatenate((this_actions_central, actions_central))
#         actions_central = np.concatenate((this_actions_central, actions_central))
#         angles_central  = np.concatenate((this_angles_central, angles_central))
#         freqs_central   = np.concatenate((this_freqs_central, freqs_central))
#         source_id       = np.concatenate((this_source_id, source_id))

#     f.close()

# fout = h5.File('central_action_catalog_all_radv_pospar'+'.h5', 'w')

# fout.create_dataset('actions_median', data=med_actions)
# fout.create_dataset('angles_median', data=med_angles)
# fout.create_dataset('freqs_median', data=med_freqs)
# fout.create_dataset('actions_central', data=actions_central)
# fout.create_dataset('angles_central', data=angles_central)
# fout.create_dataset('freqs_central', data=freqs_central)
# fout.create_dataset('posvel_median', data=med_posvel)
# fout.create_dataset('source_id', data=source_id)

# fout.close()
