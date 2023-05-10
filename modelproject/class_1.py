from types import SimpleNamespace
import random as rand
from functions_1 import *
import numpy as np
import matplotlib.pyplot as plt
import itertools

class agent:
    def __init__(self, id, max_p, curr_d_p, min_rw, curr_s_w,initial_cash=1000):
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
        self.rw_curr_surplus = 1
        self.worked = False

        # constraints
        self.cash = initial_cash



class firm:
    def __init__(self, id, min_p, curr_s_p, max_rw, curr_d_w,initial_cash=1000):
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

        # constraints
        self.cash = initial_cash
        self.stock = 0

class economy_simulation:

    def __init__(self, p_dem_func, p_sup_func,initial_p, rw_dem_func, rw_sup_func, initial_w , n_days=30, n_agents=25, n_firms=25):
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
        par.n_agents = n_agents
        par.n_firms = n_firms

        # good market parameters
        par.p_dem_func = p_dem_func
        par.p_sup_func = p_sup_func
        par.initial_p = initial_p

        # labor market parameters
        par.rw_dem_func = rw_dem_func
        par.rw_sup_func = rw_sup_func
        par.initial_w = initial_w
    
    def simulation(self,constrained=False):

        # a. setup
        par = self.par
        inflation = par.initial_p

        # b. simulations
        agents = [agent(i,par.p_dem_func(i+1),par.initial_p,par.rw_sup_func(i+1),par.initial_w) for i in range(par.n_agents)]
        firms = [firm(i,par.p_sup_func(i+1),par.initial_p,par.rw_sup_func(i+1),par.initial_w) for i in range(par.n_firms)]
        poss_comb = list(itertools.product(agents,firms))
        poss_comb = [list(comb) for comb in poss_comb]
        
        # accounting
        inflation_list = []
        wage_list = []

        # day simulation
        for day in range(par.n_days):
            print(f'day {day}:')
            day_w_list = []
            # labor market 
            rand.shuffle(poss_comb)
            for chosen_pair in poss_comb:
                # were choosing one interaction
                chosen_worker, chosen_employer = chosen_pair
                
                w = labor_market(chosen_worker,chosen_employer,inflation,constrained=constrained)

                if str(w) != "nan":
                    day_w_list.append(w)
            
            if day_w_list != []:
                w = sum(day_w_list)/len(day_w_list)
            
            wage_list.append(w)
            
            list_agents = []
            for chosen_pair in poss_comb:
                chosen_worker, chosen_employer = chosen_pair
                
                if chosen_worker not in list_agents:
                    list_agents.append(chosen_worker)
                    if not chosen_worker.worked:
                        chosen_worker.curr_w -= 1
                    else:
                        chosen_worker.worked = False

                if chosen_employer not in list_agents:
                    list_agents.append(chosen_employer)
                    if not chosen_employer.employed:
                        chosen_employer.curr_w += 1
                    else:
                        chosen_employer.employed = False




            # good market
            rand.shuffle(poss_comb)
            p_list = []
            
            
            for chosen_pair in poss_comb:
                
                # were choosing one interaction
                chosen_buyer, chosen_seller = chosen_pair
                
                p = trade(chosen_buyer,chosen_seller,do_print=True)
                
                if str(p) != "nan":
                    p_list.append(p)
            
            if p_list != []:
                inflation = sum(p_list)/len(p_list)

            print("today's price:",inflation,"Today's wage:",w,"real wage:",w/inflation)
            Demand = 0
            Supply = 0

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
                    if inflation <= chosen_buyer.max_p:
                        Demand += 1
                
                if chosen_seller not in list_agents:
                    list_agents.append(chosen_seller)
                    print(chosen_seller.cash)
                    if not chosen_seller.sold:
                        chosen_seller.curr_p -= 1
                    else:
                        chosen_seller.sold = False
                    if inflation >= chosen_seller.min_p:
                        Supply += 1
            print(Demand,Supply)

            inflation_list.append(inflation)
            
        
        return inflation_list, wage_list

            # take out after
            

            
                
            
                
                
            
            

            
        
                    