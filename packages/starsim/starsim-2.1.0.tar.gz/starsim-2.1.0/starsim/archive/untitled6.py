"""
What -- this shows no difference in the number of infections!!
"""

import numpy as np
import pylab as pl
import sciris as sc

n = 100
reps = 10_000
nc = 4
thresh = 1-(0.5/n)
sc.options(dpi=200)
pl.figure(figsize=(10,8))

d = sc.objdict(defaultdict=sc.autolist)

def matsort(arr):
    s0 = arr.sum(axis=0)
    s1 = arr.sum(axis=1)
    o0 = np.argsort(s0)
    o1 = np.argsort(s1)
    arr = arr[o1,:][:,o0]
    return arr

for rep in range(reps):

    # Truly random
    A = np.random.rand(n,n)
    A = matsort(A)
    
    # Modulo
    b1 = np.random.rand(n,1)
    b2 = np.random.rand(1,n)
    B1 = np.tile(b1, (1,n))
    B2 = np.tile(b2, (n,1))
    B = (B1 + B2) % 1.0
    B = matsort(B)
    
    # Thresholded
    At = A>thresh
    Bt = B>thresh
    v = sc.objdict()
    v.Asum = A.sum()
    v.Bsum = B.sum()
    v.Atsum = (At.sum(axis=1) > 0).sum()
    v.Btsum = (Bt.sum(axis=1) > 0).sum()
    
    for k,val in v.items():
        d[k] += val
    
    
    
#%% Plotting
labels = ['Truly random', 'Modulo']
reslabel = dict(
    Asum='Truly random, number of edge transmissions',
    Bsum='Modulo, number of edge transmissions',
    Atsum='Truly random, number of infections',
    Btsum='Modulo number of infections',
)
for i,k,val in d.enumitems():
    pl.subplot(2,2,i+1)
    pl.hist(val, bins=int(np.sqrt(reps)))
    pl.title(f'{reslabel[k]} {np.array(val).mean():n}')

sc.figlayout()
pl.show()
