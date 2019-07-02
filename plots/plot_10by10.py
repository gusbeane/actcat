import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.stats import sigmaclip
from astropy.stats import SigmaClip

def sclip(a, s=5):
    _, low0, high0 = sigmaclip(a, low=s, high=s)
    a0bool = np.logical_and(a > low0, a < high0)
    k = np.where(a0bool)[0]
    return k

sigclip = SigmaClip(5)

xrng_list = [[1.5, 7],
             [2.9, 3.6],
             [2.5, 6]]

for i, xrng in zip(range(3), xrng_list):
    fig, ax = plt.subplots(10, 10, figsize=(20,20))

    actcat = pickle.load(open('../catalog/action_catalog.pickle', 'rb'))
    keys = list(actcat.keys())

    for k, x in zip(keys, ax.ravel()):
        to_plot = sigclip(np.log10(np.abs(actcat[k]['act'][:,i])))
        x.hist(to_plot, bins=100)
        x.set_xlim(xrng)
    
    fig.tight_layout()
    fig.savefig('action_'+str(i)+'.pdf')
