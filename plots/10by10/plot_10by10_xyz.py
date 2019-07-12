import numpy as np
import matplotlib.pyplot as plt
import h5py as h
from astropy.stats import SigmaClip

sigclip = SigmaClip(5)

slice_list = [[0,1],
              [0,2],
              [1,2]]

label_list=['xy', 'xz', 'yz']

actcat = h.File('../../catalog/action_catalog.h5', 'r')

for slc, label in zip(slice_list, label_list):
    fig, ax = plt.subplots(10, 10, figsize=(20,20))

    for pvel, samples, x in zip(actcat['posvel'], actcat['actions'], ax.ravel()):
        x.scatter(pvel[:,slc[0]], pvel[:,slc[1]],
                 c=np.log10(samples[:,0]), s=0.1, cmap='hot')
    
    fig.tight_layout()
    fig.savefig('action_'+label+'.png')
