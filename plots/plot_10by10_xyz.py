import numpy as np
import matplotlib.pyplot as plt
import pickle
from astropy.stats import SigmaClip

sigclip = SigmaClip(5)

slice_list = [[0,1],
              [0,2],
              [1,2]]

label_list=['xy', 'xz', 'yz']

actcat = pickle.load(open('../catalog/action_catalog.pickle', 'rb'))
keys = list(actcat.keys())

for slc, label in zip(slice_list, label_list):
    fig, ax = plt.subplots(10, 10, figsize=(20,20))

    for k, x in zip(keys, ax.ravel()):
        x.scatter(actcat[k]['pos_vel'][:,slc[0]], actcat[k]['pos_vel'][:,slc[1]],
                 c=np.log10(actcat[k]['act'][:,0]), s=0.1, cmap='hot')
    
    fig.tight_layout()
    fig.savefig('action_'+label+'.png')
