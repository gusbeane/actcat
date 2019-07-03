import numpy as np
import matplotlib.pyplot as plt
import h5py as h
from astropy.stats import SigmaClip

sigclip = SigmaClip(5)

slice_list = [[9,10],
              [9,11],
              [10,11]]

label_list=['xy', 'xz', 'yz']

actcat = h.File('../../catalog/action_catalog.h5', 'r')
keys = list(actcat.keys())

for slc, label in zip(slice_list, label_list):
    fig, ax = plt.subplots(10, 10, figsize=(20,20))

    for k, x in zip(keys, ax.ravel()):
        x.scatter(actcat[k][:,slc[0]], actcat[k][:,slc[1]],
                 c=np.log10(actcat[k][:,0]), s=0.1, cmap='hot')
    
    fig.tight_layout()
    fig.savefig('action_'+label+'.png')
