import numpy as np
import sciris as sc
import pylab as pl

n = 100

reps = 1001
pause = 0.5
nframes = 20
nbins = n

all_diffs = sc.objdict(Random=[], Modulo=[])
sum_diffs = sc.objdict(Random=[], Modulo=[])

# Choose logarithmically spaced frames to plot
frames = np.linspace(0, np.log(reps), nframes)
frames = np.exp(frames).astype(int) - 1

sc.options(dpi=200)
fig = pl.figure(figsize=(12,8))
sc.figlayout()

for rep in range(reps):
    a = np.random.rand(n,n)
    b1 = np.random.rand(n,1)
    b2 = np.random.rand(1,n)
    B1 = np.tile(b1, (1,n))
    B2 = np.tile(b2, (n,1))
    b = (B1 + B2) % 1.0
    
    arrdict = sc.objdict(Random=a, Modulo=b)
    
    for i,key,arr in arrdict.enumitems():
    
        v1 = np.diff(arr, axis=0)
        v2 = np.diff(arr, axis=1)
        v = sc.cat(v1.flatten(), v2.flatten()).tolist()
        all_diffs[key] += v
        
        sv = np.diff(arr.sum(axis=0)).tolist()
        sum_diffs[key] += sv
    
    if rep in frames:
        fig.clear()
        for i,key,arr in arrdict.enumitems():
            
            pl.subplot(2,3,1+i*3)
            pl.imshow(arr, cmap='turbo')
            t = f'{key}: rep={rep}\nmean={arr.mean():0.3f}, std={arr.std():0.3f}\nmin={arr.min():0.3f}, max={arr.max():0.3f}'
            pl.title(t)
            
            pl.subplot(2,3,2+i*3)
            hist, bins = np.histogram(all_diffs[key], bins=nbins)
            w = np.diff(bins).mean()
            pl.bar(bins[:-1], hist, width=w, facecolor='k', lw=0)
            pl.title(f'{key}: all diffs rep={rep}')
            sc.commaticks()
            
            pl.subplot(2,3,3+i*3)
            shist, sbins = np.histogram(sum_diffs[key], bins=nbins)
            w = np.diff(sbins).mean()
            pl.bar(sbins[:-1], shist, width=w, facecolor='k', lw=0)
            pl.title(f'{key}: sum diffs rep={rep}')
            sc.commaticks()
        
        pl.pause(pause)
