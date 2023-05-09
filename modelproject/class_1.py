from types import SimpleNamespace
import random as rand
from functions_1 import trade
import numpy as np
import matplotlib.pyplot as plt
import itertools

class buyer:
    def __init__(self, id, max_p, curr_d_p, min_rw, curr_s_w):
        # identification
        self.id = id

        # good market
        self.max_p = max_p
        self.curr_p = curr_d_p
        self.p_curr_surplus = 0
        self.bought = False

        # labor market
        self.min_rw = min_rw
        self.curr_w = curr_s_w
        self.rw_curr_surplus = 0
        self.worked = False



class seller:
    def __init__(self, id, min_p, curr_s_p, max_rw, curr_d_w):
        # identification
        self.id = id

        # good market
        self.min_p = min_p
        self.curr_p = curr_s_p
        self.p_curr_surplus = 0
        self.sold = False

        # labor market
        self.max_rw = max_rw
        self.curr_w = curr_d_w
        self.rw_curr_surplus = 0
        self.employed = False

class economy_simulation:

    def __init__(self, dem_func, sup_func, initial_p, n_days=30, n_buyers=25, n_sellers=25, ):
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
        par.initial_p = initial_p
    
    def simulate(self):

        # a. setup
        par = self.par
        

        # b. simulations
        buyers = [buyer(i,par.dem_func(i+1),par.initial_p) for i in range(par.n_buyers)]
        sellers = [seller(i,par.sup_func(i+1),par.initial_p) for i in range(par.n_sellers)]
        poss_comb = list(itertools.product(buyers,sellers))
        poss_comb = [list(comb) for comb in poss_comb]

        iter = 0

        for day in range(par.n_days):
            rand.shuffle(poss_comb)

            print(f'day {day}:')
            print(poss_comb)
            for chosen_pair in poss_comb:
                
                # were choosing one interaction
                chosen_buyer, chosen_seller = chosen_pair
                
                p = trade(chosen_buyer,chosen_seller,par.n_sellers,do_print=True)

            # reset
            list_agents = []
            for chosen_pair in poss_comb:
                chosen_buyer, chosen_seller = chosen_pair
                
                if chosen_buyer not in list_agents:
                    list_agents.append(chosen_buyer)
                    if not chosen_buyer.bought:
                        chosen_buyer.curr_p += 1
                    else:
                        chosen_buyer.bought = False

                if chosen_seller not in list_agents:
                    list_agents.append(chosen_seller)
                    if not chosen_seller.sold:
                        chosen_seller.curr_p -= 1
                    else:
                        chosen_seller.sold = False
                
            
                
                
            
            

            
        
                    