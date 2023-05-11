from types import SimpleNamespace
import random as rand
from functions_1 import *
import numpy as np
import matplotlib.pyplot as plt
import itertools

class agent:
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
        self.rw_curr_surplus = 1
        self.worked = False



class firm:
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

    def __init__(self, p_dem_func=None, p_sup_func=None,initial_p=None, rw_dem_func=None, rw_sup_func=None, initial_w=None , n_days=30, n_agents=25, n_firms=25,only_goods=False,only_labor=False):
        """Creates an economy simulation
        
        Parameters:
        dem_func: demand function of the economy
        sup_func: supply function of the economy
        dem_dom: [left_bound, right_bound] it's the domain of the demand function
        sup_dom: [left_bound, right_bound] it's the domain of the supply function
        
        """
        assert (not only_goods or not only_labor)

        par = self.par = SimpleNamespace()
        
        # a. functional parameters
        par.n_days = n_days
        par.n_agents = n_agents
        par.n_firms = n_firms

        # good market parameters
        if only_labor:
            par.p_dem_func = lambda x: 1
            par.p_sup_func = lambda x: 1
            par.initial_p = initial_p
        else:
            par.p_dem_func = p_dem_func
            par.p_sup_func = p_sup_func
            par.initial_p = initial_p
        
        par.only_goods = only_goods

        # labor market parameters
        if only_goods:
            par.rw_dem_func = lambda x: 1
            par.rw_sup_func = lambda x: 1
            par.initial_w = 1
        else:
            par.rw_dem_func = rw_dem_func
            par.rw_sup_func = rw_sup_func
            par.initial_w = initial_w
        par.only_labor = only_labor
    
    def simulation(self):

        # a. setup
        par = self.par
        inflation = par.initial_p

        # b. simulations
        agents = [agent(i,par.p_dem_func(i+1),par.initial_p,par.rw_sup_func(i+1),par.initial_w) for i in range(par.n_agents)]
        firms = [firm(i,par.p_sup_func(i+1),par.initial_p,par.rw_dem_func(i+1),par.initial_w) for i in range(par.n_firms)]
        poss_comb = list(itertools.product(agents,firms))
        poss_comb = [list(comb) for comb in poss_comb]
        
        # accounting
        inflation_list = []
        wage_list = []
        g_demand_list = []
        g_supply_list = []
        l_demand_list = []
        l_supply_list = []

        # day simulation
        for day in range(par.n_days):
            print(f'day {day}:')
            
            l_Supply = 0
            l_Demand = 0

            if not par.only_goods:
                day_w_list = []
                # labor market 
                rand.shuffle(poss_comb)
                for chosen_pair in poss_comb:
                    # were choosing one interaction
                    chosen_worker, chosen_employer = chosen_pair
                    inter_w = labor_market(chosen_worker,chosen_employer,inflation,do_print=True)

                    if str(inter_w) != "nan":
                        day_w_list.append(inter_w)
                
                if day_w_list != []:
                    day_w = sum(day_w_list)/len(day_w_list)
                else:
                    day_w = np.nan
                
                # clearing up all the nans
                if str(day_w) == "nan":
                    if day == 0:
                        day_w = par.initial_w
                    else:
                        day_w = wage_list[-1]

                wage_list.append(day_w)
                
                list_agents = []
                for chosen_pair in poss_comb:
                    chosen_worker, chosen_employer = chosen_pair
                    
                    if chosen_worker not in list_agents:
                        list_agents.append(chosen_worker)
                        if not chosen_worker.worked:
                            chosen_worker.curr_w -= 1
                        else:
                            chosen_worker.worked = False
                        if day_w > int(chosen_worker.min_rw*inflation)+1:
                            l_Supply += 1

                    if chosen_employer not in list_agents:
                        list_agents.append(chosen_employer)
                        if not chosen_employer.employed:
                            chosen_employer.curr_w += 1
                        else:
                            chosen_employer.employed = False
                        if day_w < int(chosen_employer.max_rw*inflation):
                            l_Demand += 1
                
                l_demand_list.append(l_Demand)
                l_supply_list.append(l_Supply)


            if not par.only_labor:
                # good market
                rand.shuffle(poss_comb)
                p_list = []
                
                
                for chosen_pair in poss_comb:
                    
                    # were choosing one interaction
                    chosen_buyer, chosen_seller = chosen_pair
                    
                    p = trade(chosen_buyer,chosen_seller)
                    
                    if str(p) != "nan":
                        p_list.append(p)
                
                if p_list != []:
                    inflation = sum(p_list)/len(p_list)

                
                g_Demand = 0
                g_Supply = 0

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
                        if inflation < chosen_buyer.max_p:
                            g_Demand += 1
                    
                    if chosen_seller not in list_agents:
                        list_agents.append(chosen_seller)
                        if not chosen_seller.sold:
                            chosen_seller.curr_p -= 1
                        else:
                            chosen_seller.sold = False
                        if inflation > chosen_seller.min_p:
                            g_Supply += 1

                inflation_list.append(inflation)
                g_demand_list.append(g_Demand)
                g_supply_list.append(g_Supply)
                
                ending_phrase = ""
                
                if not par.only_labor:
                    ending_phrase += f"Today's price: {inflation}, D: {g_Demand}, S: {g_Supply}"
                    if not par.only_goods:
                        ending_phrase += ", "
                if not par.only_goods:
                    ending_phrase += f"Today's wage: {day_w}, Real wage: {day_w/inflation}, D: {l_Demand}, S: {l_Supply}"

                print(ending_phrase)
                
        if par.only_goods:
            return inflation_list, g_demand_list, g_supply_list
        elif par.only_labor:
            return wage_list, l_demand_list, l_supply_list
        else:
            return inflation_list,g_demand_list, g_supply_list, wage_list, l_demand_list, l_supply_list

            # take out after
            

            
                
            
                
                
            
            

            
        
                    