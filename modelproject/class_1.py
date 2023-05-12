from types import SimpleNamespace
import random as rand
from functions_1 import *
import numpy as np
import matplotlib.pyplot as plt
import itertools

class person:
    def __init__(self, id, max_p, curr_d_p, min_rw, curr_s_w):
        # a. identification
        self.id = id

        # b. good market parameters
        self.max_p = max_p
        self.curr_p = curr_d_p
        self.p_curr_surplus = 0
        self.bought = False

        # c. labor market parameters
        self.min_rw = min_rw
        self.curr_w = curr_s_w
        self.rw_curr_surplus = 1
        self.worked = False



class firm:
    def __init__(self, id, min_p, curr_s_p, max_rw, curr_d_w):
        # a. identification
        self.id = id

        # b. good market parameters
        self.min_p = min_p
        self.curr_p = curr_s_p
        self.p_curr_surplus = 0
        self.sold = False

        # c. labor market parameters
        self.max_rw = max_rw
        self.curr_w = curr_d_w
        self.rw_curr_surplus = 0
        self.employed = False

class economy_simulation:

    def __init__(self, p_dem_func=None, p_sup_func=None,initial_p=None, rw_dem_func=None, rw_sup_func=None, initial_w=None , n_days=30, n_persons=25, n_firms=25,only_goods=False,only_labor=False):
        """Creates an economy simulation
        
        Parameters:
        
        Good market:
        p_dem_func: function; good demand function of the economy
        p_sup_func: function; good supply function of the economy
        initial_p: int; initial price of the economy

        Labor market:
        rw_dem_func: function; labor demand function of the economy, in real wage terms
        rw_dem_func: function; labor supply function of the economy, in real wage terms
        initial_w: int; in nominal wage terms

        Simulation:
        n_days: int; number of simulation days
        n_persons: int; number of simulated persons
        n_firms: int; number of simulated firms

        Other:
        only_goods: bool; If true, only the good market will be simulated, and you don't need to input the Labor Market Parameters.
        only_labor: bool; If true, only the labor market will be simulated and you don't need to input the Good Market Parameters (except the initial price).
        """
        # a. error handling
        assert (not only_goods or not only_labor)
        if not only_goods:
            assert rw_dem_func != None and rw_sup_func != None and initial_w != None, initial_p != None
        if not only_labor:
            assert p_dem_func != None and p_sup_func != None and initial_p != None

        # b. initiate parameters
        par = self.par = SimpleNamespace()
        
        # c. functional parameters
        par.n_days = n_days
        par.n_persons = n_persons
        par.n_firms = n_firms

        # d. good market parameters
        if only_labor:
            
            # i. placeholder, when goods market not needed
            par.p_dem_func = lambda x: 1
            par.p_sup_func = lambda x: 1
            par.initial_p = initial_p
        
        else:
            par.p_dem_func = p_dem_func
            par.p_sup_func = p_sup_func
            par.initial_p = initial_p
        
        par.only_goods = only_goods

        # e. labor market parameters
        if only_goods:

            # ii. placeholder, when labor market not needed
            par.rw_dem_func = lambda x: 1
            par.rw_sup_func = lambda x: 1
            par.initial_w = 1

        else:
            par.rw_dem_func = rw_dem_func
            par.rw_sup_func = rw_sup_func
            par.initial_w = initial_w

        par.only_labor = only_labor
    
    def simulation(self,do_print=False):

        # a. setup
        par = self.par
        inflation = par.initial_p

        # b. simulations
        persons = [person(i,par.p_dem_func(i+1),par.initial_p,par.rw_sup_func(i+1),par.initial_w) for i in range(par.n_persons)]
        firms = [firm(i,par.p_sup_func(i+1),par.initial_p,par.rw_dem_func(i+1),par.initial_w) for i in range(par.n_firms)]
        
        # c. create every single combination of persons and firms
        poss_comb = list(itertools.product(persons,firms))
        poss_comb = [list(comb) for comb in poss_comb]
        
        # d. accounting setup
        inflation_list = []
        wage_list = []
        g_demand_list = []
        g_supply_list = []
        l_demand_list = []
        l_supply_list = []

        # e. day simulation
        for day in range(par.n_days):
            
            # i. labor supply and demand accounting setup
            l_Supply = 0
            l_Demand = 0

            # ii. initiate the labor market
            if not par.only_goods:
                
                # 1. accounting for all interaction's equilibrium wages
                day_w_list = []

                # 2. shuffle the combinations 
                rand.shuffle(poss_comb)

                # 3. doing all interactions
                for chosen_pair in poss_comb:

                    chosen_worker, chosen_employer = chosen_pair
                    inter_w = labor_market(chosen_worker,chosen_employer,inflation)

                    # o. cleaning all the unsuccessful interactions
                    if str(inter_w) != "nan":
                        day_w_list.append(inter_w)
                
                # 4. calculate today's average wage and store it
                if day_w_list != []:
                    day_w = sum(day_w_list)/len(day_w_list)
                
                else:
                    if day == 0:
                        day_w = par.initial_w
                    
                    else:
                        day_w = wage_list[-1]
   
                wage_list.append(day_w)

                # 5. update all parameters and calculate demand and supply
                list_persons = []
                
                for chosen_pair in poss_comb:
                    chosen_worker, chosen_employer = chosen_pair
                    
                    if chosen_worker not in list_persons:
                        list_persons.append(chosen_worker)
                        
                        # o. update workers
                        if not chosen_worker.worked:
                            chosen_worker.curr_w -= 1
                        else:
                            chosen_worker.worked = False
                        
                        # oo. calculate labor supply
                        if day_w >= int(chosen_worker.min_rw*inflation)+1:
                            l_Supply += 1

                    if chosen_employer not in list_persons:
                        list_persons.append(chosen_employer)
                        
                        # o. update employers
                        if not chosen_employer.employed:
                            chosen_employer.curr_w += 1
                        else:
                            chosen_employer.employed = False
                        
                        # oo. calculate labor demand
                        if day_w <= int(chosen_employer.max_rw*inflation):
                            l_Demand += 1
                
                # 6. store labor demand and supply
                l_demand_list.append(l_Demand)
                l_supply_list.append(l_Supply)

            # iii. goods supply and demand accounting setup
            g_Demand = 0
            g_Supply = 0

            # iv. initiate goods market
            if not par.only_labor:
                # 1. accounting for all interaction's equilibrium prices
                p_list = []
                
                # 2. shuffle the combinations
                rand.shuffle(poss_comb)
                
                # 3. doing all interactions
                for chosen_pair in poss_comb:
                    
                    chosen_buyer, chosen_seller = chosen_pair
                    p = trade(chosen_buyer,chosen_seller)
                    
                    # o. cleaning all the unsuccessful interactions
                    if str(p) != "nan":
                        p_list.append(p)
                
                # 4. calculate today's average price and store it
                if p_list != []:
                    inflation = sum(p_list)/len(p_list)

                inflation_list.append(inflation)

                # 5. update all parameters and calculate demand and supply
                list_persons = []

                for chosen_pair in poss_comb:
                    chosen_buyer, chosen_seller = chosen_pair
                    
                    if chosen_buyer not in list_persons:
                        list_persons.append(chosen_buyer)
                        
                        # o. update buyers
                        if not chosen_buyer.bought:
                            chosen_buyer.curr_p += 1
                        else:
                            chosen_buyer.bought = False
                        
                        # oo. calculate goods demand
                        if inflation <= chosen_buyer.max_p:
                            g_Demand += 1
                    
                    if chosen_seller not in list_persons:
                        list_persons.append(chosen_seller)
                        
                        # o. update sellers
                        if not chosen_seller.sold:
                            chosen_seller.curr_p -= 1
                        else:
                            chosen_seller.sold = False
                        
                        # oo. calculate goods supply
                        if inflation >= chosen_seller.min_p:
                            g_Supply += 1

                # 6. store goods demand and supply
                g_demand_list.append(g_Demand)
                g_supply_list.append(g_Supply)
                
            # v. printing message
            if do_print:
                print(f'day {day}:')

                ending_phrase = ""
                
                # i. goods market
                if not par.only_labor:
                    ending_phrase += f"Today's price: {inflation:.0f}, D: {g_Demand}, S: {g_Supply}"
                    
                    if not par.only_goods:
                        ending_phrase += "\n"
                
                # ii. labor market
                if not par.only_goods:
                    ending_phrase += f"Today's wage: {day_w:.0f}, Real wage: {day_w/inflation:.2f}, D: {l_Demand}, S: {l_Supply}"

                print(ending_phrase)

        # f. output handling   
        if par.only_goods:
            return inflation_list, g_demand_list, g_supply_list
        
        elif par.only_labor:
            return wage_list, l_demand_list, l_supply_list
        
        else:
            return inflation_list,g_demand_list, g_supply_list, wage_list, l_demand_list, l_supply_list
            

            
                
            
                
                
            
            

            
        
                    