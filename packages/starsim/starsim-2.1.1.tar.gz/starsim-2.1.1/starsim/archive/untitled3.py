import os
import numpy as np
import sciris as sc
import starsim as ss
import pylab as pl

reps = 10_000
keys = {'0.5.2':'modulo', '0.5.3':'roulette'}
filenames = {k:f'rng_stat_{k}.json' for k in keys.values()}


def make_sim(seed):
    pars = dict(
        rand_seed = seed,
        n_agents = 1000,
        end = 2020,
        diseases = ['sir', 'sis'],
        networks = 'random',
        verbose = 0,
    )
    sim = ss.Sim(pars)
    return sim

def run_sim_summary(seed):
    sim = make_sim(seed)
    sim.run()
    return sim.summary

def plot_sim():
    sim = make_sim()
    fig = sim.run().plot()
    return fig

def run_sims():
    ver = ss.__version__
    sc.heading(f'Running {ver}...')
    T = sc.timer()
    reslist = sc.parallelize(run_sim_summary, np.arange(reps))
    res = dict()
    for k in reslist[0].keys():
        res[k] = []
    for entry in reslist:
        for k in res.keys():
            res[k].append(entry[k])
    key = keys[ver]
    filename = filenames[key]
    sc.savejson(filename, res)
    T.toc()
    return

def get_raw():
    raw = sc.objdict()
    for k,filename in filenames.items():
        if not os.path.exists(filename):
            run_sims()
            print('Now change branch (if needed) and re-run')
            break
        raw[k] = sc.loadjson(filename)
    return raw

def get_res(raw):
    res = sc.objdict()
    for k,v in raw.items():
        res[k] = sc.objdict()
        for k2,v2 in v.items():
            mean = np.mean(v2)
            sem = np.std(v2)/np.sqrt(len(v2))
            res[k][k2] = sc.objdict(mean=mean, sem=sem)
    return res

def plot(raw, res):
    keys = res[0].keys()
    nkeys = len(keys)
    
    sc.options(dpi=150)
    fig = pl.figure(figsize=(16,16))
    count = 0
    for i,k in enumerate(keys):
        mod = res.modulo[k]
        rou = res.roulette[k]
        z = 2
        modmin = mod.mean - z*mod.sem
        modmax = mod.mean + z*mod.sem
        roumin = rou.mean - z*rou.sem
        roumax = rou.mean + z*rou.sem
        statsig = True if (modmax < roumin) or (modmin > roumax) else False
        for i2,k2 in enumerate(res.keys()):
            count += 1
            this = res[k2][k]
            title = f'{k2}\n{k}\n{this.mean:n}±{2*this.sem:n}'
            if statsig:
                title += '\n(mismatch!)'
            pl.subplot(nkeys//2,4,count)
            pl.hist(raw[k2][k], bins=int(np.sqrt(reps)))
            pl.title(title)
        
    sc.figlayout()
    pl.show()
    return fig
    
    
if __name__ == '__main__':
    raw = get_raw()
    res = get_res(raw)
    fig = plot(raw, res)