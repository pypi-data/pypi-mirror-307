import numpy as np
import sciris as sc
import pylab as pl

n = 50
seed = 1
reps = 1001
pause = 0.5
nframes = 20
nbins = n

np.random.seed(seed)
all_diffs = sc.objdict(Random=[], Modulo=[], Roulette=[])
row_diffs = sc.dcp(all_diffs)

# Choose logarithmically spaced frames to plot
frames = np.linspace(0, np.log(reps), nframes)
frames = np.exp(frames).astype(int) - 1

sc.options(dpi=200)
fig = pl.figure(figsize=(12,10))
sc.figlayout()


for rep in range(reps):
    
    # Truly random
    A = np.random.rand(n,n)
    
    # Modulo
    b1 = np.random.rand(n,1)
    b2 = np.random.rand(1,n)
    B1 = np.tile(b1, (1,n))
    B2 = np.tile(b2, (n,1))
    B = (B1 + B2) % 1.0
    
    # Roulette
    c1 = np.random.rand(n,1)
    C1 = np.tile(c1, (1,n))
    C2 = np.random.rand(n,n)
    C2 = C2*n/C2.sum(axis=0)
    C = C1*C2
    
    arrdict = sc.objdict(Random=A, Modulo=B, Roulette=C)
    
    for i,key,arr in arrdict.enumitems():
    
        v1 = np.diff(arr, axis=0)
        v2 = np.diff(arr, axis=1)
        v = sc.cat(v1.flatten(), v2.flatten()).tolist()
        all_diffs[key] += v
        
        rd = np.diff(arr.sum(axis=1)).tolist()
        row_diffs[key] += rd
    
    if rep in frames:
        fig.clear()
        for i,key,arr in arrdict.enumitems():
            
            pl.subplot(3,3,1+i*3)
            pl.imshow(arr, cmap='turbo')
            t = f'{key}: rep={rep}\nmean={arr.mean():0.3f}, std={arr.std():0.3f}\nmin={arr.min():0.3f}, max={arr.max():0.3f}'
            pl.title(t)
            
            pl.subplot(3,3,2+i*3)
            hist, bins = np.histogram(all_diffs[key], bins=nbins)
            w = np.diff(bins).mean()
            pl.bar(bins[:-1], hist, width=w, facecolor='k', lw=0)
            pl.title(f'{key}: all diffs rep={rep}')
            sc.commaticks()
            
            pl.subplot(3,3,3+i*3)
            rhist, rbins = np.histogram(row_diffs[key], bins=nbins)
            w = np.diff(rbins).mean()
            pl.bar(rbins[:-1], rhist, width=w, facecolor='k', lw=0)
            pl.title(f'{key}: row diffs rep={rep}')
            sc.commaticks()
        
        pl.pause(pause)
