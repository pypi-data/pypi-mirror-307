import numpy as np
import sciris as sc
import pylab as pl
# import numba as nb

# @nb.njit # No faster -- not sure why not
def get_probs(n, inds, trg, trans_prob):
    probs = np.ones(n)
    trg_inds = trg[inds]
    for trg_ind in trg_inds:
        probs[trg_ind] *= (1-trans_prob)
    probs = 1 - probs
    return probs

# PARAMETERS
p = sc.objdict(
    n = 100, # Number of nodes
    n_sources = 2, # Number of sources (seed infections)
    edge_prob = 0.1, # Edge probability
    trans_prob = 0.05,
    seed = 6,
    npts = 10,
)


class Sim:
    def __init__(self, p, method='random', repseed=0):
        self.p = p
        self.repseed = repseed
        self.method = method
        self.initialize()
        self.make_network()
    
    def initialize(self):
        np.random.seed(self.p.seed+self.repseed)
        n = self.p.n
        self.uids = np.arange(n)
        self.inf = np.zeros(n, dtype=int)
        self.inf[0:self.p.n_sources] = 1
        self.xpos = np.random.rand(n)
        self.ypos = np.random.rand(n)
        self.t = 0
        self.tvec = np.arange(p.npts+1)
        self.n_infected = p.n_sources*np.ones(p.npts+1)

    def make_network(self):
        p = self.p
        n_possible = p.n**2
        n_edges = np.random.binomial(n_possible, p.edge_prob)
        p1 = np.random.choice(self.uids, size=n_edges)
        p2 = np.random.choice(self.uids, size=n_edges)
        self.src = sc.cat(p1, p2) # Bidirectional transmission
        self.trg = sc.cat(p2, p1)
        
    def get_edges(self):
        possible = (self.inf[self.src]==1) * (self.inf[self.trg]==0)
        inds = sc.findinds(possible)
        return inds
    
    def trans_rand(self, inds):
        r = np.random.rand(len(inds))
        trans = self.p.trans_prob > r
        trans_inds = inds[trans]
        inf_inds = self.trg[trans_inds]
        return inf_inds
    
    def trans_modulo(self, inds):
        r1 = np.random.rand(self.p.n)
        r2 = np.random.rand(self.p.n)
        # np.random.shuffle(r2)
        r1 = r1[self.src[inds]]
        r2 = r2[self.trg[inds]]
        r = (r1 + r2) % 1.0
        trans = self.p.trans_prob > r
        trans_inds = inds[trans]
        inf_inds = self.trg[trans_inds]
        return inf_inds
    
    def trans_roulette(self, inds):
        trans_prob = self.p.trans_prob
        n = self.p.n
        trg = self.trg
        probs = get_probs(n, inds, trg, trans_prob)
        r = np.random.rand(self.p.n)
        inf_inds = probs > r
        return inf_inds
        
    def step(self):
        self.t += 1
        inds = self.get_edges()
        if self.method == 'random':
            inf_inds = self.trans_rand(inds)
        elif self.method == 'roulette':
            inf_inds = self.trans_roulette(inds)
        elif self.method == 'modulo':
            inf_inds = self.trans_modulo(inds)
        else:
            raise Exception('Method not found')
        self.inf[inf_inds] = True
        self.n_infected[self.t] = self.inf.sum()
            
    def run(self):
        for t in range(self.p.npts):
            self.step()
            if self.n_infected[self.t] == self.p.n:
                self.n_infected[self.t+1:] = self.p.n
                break
        return
            
    def plot_network(self):
        fig = pl.figure()
        x = self.xpos
        y = self.ypos
        inf = self.inf == 1
        ninf = self.inf == 0
        pl.scatter(x[ninf], y[ninf], c='green')
        pl.scatter(x[inf], y[inf], c='red')
        for p1,p2 in zip(self.src, self.trg):
            pl.plot([x[p1], x[p2]], [y[p1], y[p2]], alpha=0.2, c='k', lw=0.1)
        return fig
    
    def plot(self):
        fig = pl.figure()
        pl.plot(self.tvec, self.n_infected)
        return fig


def run_sim(sim):
    sim.run()
    return sim


class MultiSim:
    def __init__(self, p, method='random', reps=10):
        self.p = p
        self.method = method
        self.reps = reps
        self.initialize()
    
    def initialize(self):
        self.sims = [Sim(p=self.p, method=self.method, repseed=rep) for rep in range(self.reps)]
    
    def run(self):
        self.sims = sc.parallelize(run_sim, self.sims)
        self.results = np.zeros((self.p.npts+1, self.reps))
        for i,sim in enumerate(self.sims):
            self.results[:,i] = sim.n_infected
        
    def plot_all(self):
        pl.figure()
        pl.plot(self.results, alpha=0.2)
    
    def plot_stats(self, ax=None):
        if ax is None:
            fig,ax = pl.subplots(1)
        pl.sca(ax)
        qs = [0, 0.0025, 0.01, 0.05, 0.1, 0.25]
        res = self.results
        mean = res.mean(axis=1)
        std = res.std(axis=1)
        x = np.arange(len(mean))
        for q in qs:
            low = np.quantile(res, q, axis=1)
            high = np.quantile(res, 1-q, axis=1)
            pl.fill_between(x, low, high, alpha=0.1, facecolor='red')
        pl.plot(mean, 'o-', c='k', lw=2)
        pl.xlabel('Timestep')
        pl.ylabel('Number infected')
        pl.title(f'Method: {self.method}; stats: μ={mean.mean():0.4f}, σ={std.mean():0.4f}')
        pl.xlim(left=0, right=p.npts)
        pl.ylim(bottom=0, top=p.n)
        
        
if __name__ == '__main__':
    sc.options(dpi=200)
    T = sc.timer()
    fig, axes = pl.subplots(1,3, figsize=(18,8))
    for m,method in enumerate(['random', 'roulette', 'modulo']):
        msim = MultiSim(p=p, method=method, reps=1_000)
        T.tic()
        msim.run()
        T.toc(method)
        msim.plot_stats(ax=axes[m])
    sc.figlayout()
    pl.show()