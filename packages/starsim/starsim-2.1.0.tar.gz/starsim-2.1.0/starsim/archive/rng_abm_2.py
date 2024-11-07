import numpy as np
import sciris as sc
import pylab as pl

# PARAMETERS
p = sc.dictobj(
    n = 10, # Number of nodes
    n_sources = 2, # Number of sources (seed infections)
    edge_prob = 0.2, # Edge probability
    trans_prob = 0.05,
    seed = 94895,
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
        r_src = np.random.rand(self.p.n*10)
        r_trg = np.random.rand(self.p.n*10)
        new = np.random.rand(self.p.n*10)
        src_inds = self.src[inds]*5
        trg_inds = self.trg[inds]
        comb_inds = (10*self.p.n-src_inds+trg_inds) % self.p.n*10
        new_inds = np.random.randint(0,self.p.n,len(inds))
        r1 = r_src[src_inds]
        r2 = r_trg[trg_inds]
        r3 = r_src[comb_inds]
        r4 = r_trg[comb_inds]
        r5 = new[comb_inds]
        r = (r1 + r2 + r3 + r4 + r5) % 1.0
        trans = self.p.trans_prob > r
        trans_inds = inds[trans]
        inf_inds = self.trg[trans_inds]
        return inf_inds
    
    def trans_roulette(self, inds):
        trans_prob = self.p.trans_prob
        probs = np.ones(self.p.n)
        for ind in inds:
            probs[self.trg[ind]] *= (1-trans_prob)
        probs = 1 - probs
        r = np.random.rand(self.p.n)
        inf_inds = probs > r
        return inf_inds
        
    def step(self):
        self.t += 1
        inds = self.get_edges()
        if self.method == 'random':
            inf_inds = self.trans_rand(inds)
        elif self.method == 'modulo':
            inf_inds = self.trans_modulo(inds)
        elif self.method == 'roulette':
            inf_inds = self.trans_roulette(inds)
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
        self.sims = sc.parallelize(run_sim, self.sims, parallelizer='thread')
        self.results = np.zeros((self.p.npts+1, self.reps))
        for i,sim in enumerate(self.sims):
            self.results[:,i] = sim.n_infected
        
    def plot_all(self):
        pl.figure()
        pl.plot(self.results, alpha=0.2)
    
    def plot_stats(self):
        pl.figure()
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
        pl.title(f'Method: {self.method}; stats: μ={mean.mean():0.4f}, σ={std.mean():0.4f}')
        
        
if __name__ == '__main__':
    
    sc.options(dpi=200)
    T = sc.timer()
    for method in ['random', 'modulo', 'roulette']:
        T.tic()
        msim = MultiSim(p=p, method=method, reps=1_000)
        msim.run()
        T.toc(method)
        msim.plot_stats()
    pl.show()