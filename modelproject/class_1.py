from types import SimpleNamespace
import random as rand
from part_1.functions_1 import trade
import numpy as np
import matplotlib.pyplot as plt

class agent:
    def __init__(self, id, max_p, cash):
        self.id = id
        self.max_p = max_p
        self.cash = cash

class firm:
    def __init__(self, id, min_p, cash):
        self.id = id
        self.min_p = min_p
        self.cash = cash

class economy_simulation:

    def __init__(self, n_sim=100, n_days=30, n_actions=1, n_agents=25, n_firms=25):
    
        par = self.par = SimpleNamespace()
        
        # a. functional parameters
        par.n_sim = n_sim
        par.n_days = n_days
        par.n_actions = n_actions
        par.n_agents = n_agents
        par.n_firms = n_firms
    
    def simulate(self):

        # a. setup
        par = self.par
        all_p = np.zeros((par.n_sim,par.n_days))
        average_p = []

        # b. simulations
        for sim in range(par.n_sim):
            agents = [agent(i,rand.randint(1,10),100) for i in range(par.n_agents)]
            firms = [firm(i,rand.randint(1,10),100) for i in range(par.n_firms)]
            agents = agents * par.n_actions
            
            for day in range(par.n_days):
                rand.shuffle(agents)
                day_p_val = []
            
                # i. Simulate each turn
                for agent_turn in agents:
                    chosen_firm = rand.choice(firms)
                    p = trade(agent_turn, chosen_firm)
                    day_p_val.append(p)
            
                all_p[sim,day] = np.nanmean(day_p_val)
            
            # ii. plot each simulation        
            plt.plot(all_p[sim], alpha=0.07,color="black")
                
        # c. calculate and plot average prices
        for day in range(par.n_days):
            average_p.append(np.nanmean(all_p[:,day]))    

        plt.plot(average_p, alpha=0.7,color="red")

        # d. print ending average price
        print(f"The average ending price is: {average_p[-1]}")