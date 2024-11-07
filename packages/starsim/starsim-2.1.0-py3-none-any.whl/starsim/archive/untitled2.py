import starsim as ss
import pandas as pd

# Read in age-specific fertility rates
fertility_rates = pd.read_csv('/home/cliffk/idm/starsim/docs/tutorials/test_data/nigeria_asfr.csv')
pregnancy = ss.Pregnancy(pars={'fertility_rate': fertility_rates})

death_rates = pd.read_csv('/home/cliffk/idm/starsim/docs/tutorials/test_data/nigeria_deaths.csv')
death = ss.Deaths(pars={'death_rate': death_rates, 'units': 1})

demographics = [pregnancy, death]

# Make people using the distribution of the population by age/sex in 1995
n_agents = 5_000
nga_pop_1995 = 106819805  # Population of Nigeria in 1995, the year we will start the model
age_data = pd.read_csv('/home/cliffk/idm/starsim/docs/tutorials/test_data/nigeria_age.csv')
ppl = ss.People(n_agents, age_data=age_data)

# Make the sim, run and plot
sim = ss.Sim(total_pop=nga_pop_1995, start=1995, people=ppl, demographics=demographics, networks='random', diseases='sir')
sim.run()

# Read in a file with the actual population size
nigeria_popsize = pd.read_csv('/home/cliffk/idm/starsim/docs/tutorials/test_data/nigeria_popsize.csv')
data = nigeria_popsize[(nigeria_popsize.year >= 1995) & (nigeria_popsize.year <= 2030)]

# Plot the overall population size - simulated vs data
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)
ax.scatter(data.year, data.n_alive, alpha=0.5, label='Data')
ax.plot(sim.yearvec, sim.results.n_alive, color='k', label='Model')
ax.legend()
ax.set_title('Population')
plt.show();
