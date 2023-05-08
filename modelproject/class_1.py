from types import SimpleNamespace
import random as rand
from functions_1 import trade
import numpy as np
import matplotlib.pyplot as plt
import itertools

class buyer:
    def __init__(self, id, max_p, curr_d_p):
        self.id = id
        self.max_p = max_p
        self.curr_p = curr_d_p
        self.curr_surplus = 0
        self.bought = False

class seller:
    def __init__(self, id, min_p, curr_s_p):
        self.id = id
        self.min_p = min_p
        self.curr_p = curr_s_p
        self.curr_surplus = 0
        self.sold = False

class economy_simulation:

    def __init__(self, dem_func, sup_func, initial_p, dem_dom=[0,1], sup_dom=[0,1], n_days=30, n_buyers=25, n_sellers=25, ):
        """Creates an economy simulation
        
        Parameters:
        dem_func: demand function of the economy
        sup_func: supply function of the economy
        dem_dom: [left_bound, right_bound] it's the domain of the demand function
        sup_dom: [left_bound, right_bound] it's the domain of the supply function
        
        """


        par = self.par = SimpleNamespace()
        
        # a. functional parameters
        par.n_days = n_days
        par.n_buyers = n_buyers
        par.n_sellers = n_sellers
        par.dem_func = dem_func
        par.sup_func = sup_func
        par.dem_dom = dem_dom
        par.sup_dom = sup_dom
        par.initial_p = initial_p
    
    def simulate(self):

        # a. setup
        par = self.par
        

        # b. simulations
        buyers = [buyer(i,par.dem_func(i),par.initial_p) for i in np.linspace(par.dem_dom[0],par.dem_dom[1], par.n_buyers)]
        sellers = [seller(i,par.sup_func(i),par.initial_p) for i in np.linspace(par.sup_dom[0],par.sup_dom[1], par.n_sellers)]
        poss_comb = list(itertools.product(buyers,sellers))
        for i, comb in enumerate(poss_comb):
            poss_comb[i] = list(comb)

        iter = 0

        for day in range(par.n_days):
            rand.shuffle(poss_comb)

            print("New day")
            print(poss_comb)
            for chosen_pair in poss_comb:
                
                # were choosing one interaction
                chosen_buyer, chosen_seller = chosen_pair
                
                p = trade(chosen_buyer,chosen_seller,par.n_sellers)

                print(p)
                
                
            
            # reset
            for i in len(poss_comb):
                poss_comb[i][0].bought = False
                poss_comb[i][1].sold = False

            
        
                    