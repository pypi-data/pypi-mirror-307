import numpy as np
import pylab as pl
import sciris as sc

n = 100
reps = 5
nc = 4
thresh = 1-(0.5/n)
sc.options(dpi=200)
pl.figure(figsize=(12,12))

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
    Asum = A.sum()/n**2
    Bsum = B.sum()/n**2
    Atsum = (At.sum(axis=1) > 0).sum()
    Btsum = (Bt.sum(axis=1) > 0).sum()
    
    
    #%% Plotting
    pl.subplot(reps,nc,1+nc*rep)
    pl.imshow(A)
    pl.title(f'Truly random {Asum:n}')
    
    pl.subplot(reps,nc,2+nc*rep)
    pl.imshow(B)
    pl.title(f'Modulo {Bsum:n}')
    
    
    pl.subplot(reps,nc,3+nc*rep)
    pl.imshow(At)
    pl.title(f'Truly random {At.sum()}→{Atsum}')
    
    pl.subplot(reps,nc,4+nc*rep)
    pl.imshow(B>thresh)
    pl.title(f'Modulo {Bt.sum()}→{Btsum}')

sc.figlayout()
pl.show()
