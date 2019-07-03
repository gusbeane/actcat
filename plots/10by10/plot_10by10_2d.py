import numpy as np
import matplotlib.pyplot as plt
import h5py as h
from scipy.stats import sigmaclip
from astropy.stats import SigmaClip

def sclip(a, s=5):
    _, low0, high0 = sigmaclip(a, low=s, high=s)
    a0bool = np.logical_and(a > low0, a < high0)
    k = np.where(a0bool)[0]
    return k

sigclip = SigmaClip(5)

yrng_list = [[1.5, 7],
             [2.5, 6]]

xrng = [2.9, 3.6]

actcat = h.File('../../catalog/action_catalog.h5', 'r')
keys = list(actcat.keys())

for i, yrng in zip([0,2], yrng_list):
    fig, ax = plt.subplots(10, 10, figsize=(20,20))

    for k, x in zip(keys, ax.ravel()):
        to_plot_x = sigclip((np.abs(actcat[k][:,1])))
        to_plot_y = sigclip((np.abs(actcat[k][:,i])))
        x.scatter(to_plot_x, to_plot_y, s=0.5)
        # x.set_xlim(xrng)
        # x.set_ylim(yrng)
    
    fig.tight_layout()
    fig.savefig('action_'+'1x'+str(i)+'.png')
