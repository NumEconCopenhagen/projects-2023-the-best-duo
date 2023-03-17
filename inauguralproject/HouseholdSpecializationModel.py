
from types import SimpleNamespace

import numpy as np
from scipy import optimize

import pandas as pd 
import matplotlib.pyplot as plt

class HouseholdSpecializationModelClass:

    def __init__(self):
        """ setup model """

        # a. create namespaces
        par = self.par = SimpleNamespace()
        sol = self.sol = SimpleNamespace()

        # b. preferences
        par.rho = 2.0        #//p
        par.nu = 0.001       #//v
        par.epsilon = 1.0    #//e
        par.omega = 0.5      #//w

        # c. household production
        par.alpha = 0.5      #//a
        par.sigma = 1.0      #//o

        # d. wages
        par.wM = 1.0
        par.wF = 1.0
        par.wF_vec = np.linspace(0.8,1.2,5) #//setup for 2 and 3

        # e. targets
        par.beta0_target = 0.4      
        par.beta1_target = -0.1

        # f. solution
        sol.LM_vec = np.zeros(par.wF_vec.size)
        sol.HM_vec = np.zeros(par.wF_vec.size)
        sol.LF_vec = np.zeros(par.wF_vec.size)
        sol.HF_vec = np.zeros(par.wF_vec.size)

        sol.beta0 = np.nan
        sol.beta1 = np.nan

    def calc_utility(self,LM,HM,LF,HF):
        """ calculate utility """

        par = self.par
        sol = self.sol

        # a. consumption of market goods
        C = par.wM*LM + par.wF*LF

        # b. home production
        if par.sigma == 0:
            H = np.fmin(LM,HM)
        
        elif par.sigma == 1:
            H = HM**(1-par.alpha) * HF**par.alpha
        
        else:
            H = ((1-par.alpha)*HM**((par.sigma-1)/par.sigma)
                 + par.alpha*HF**((par.sigma-1)/par.sigma)) ** (par.sigma/(par.sigma-1))

        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho)   #//this puts a lower bound on Q such that it never is 0

        # d. disutility of work
        epsilon_ = 1+1/par.epsilon
        TM = LM+HM
        TF = LF+HF
        disutility = par.nu*(TM**epsilon_/epsilon_+TF**epsilon_/epsilon_)
        
        return utility - disutility

    def solve_discrete(self,do_print=False):
        """ solve model discretely """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()
        
        # a. all possible choices
        x = np.linspace(0,24,49)
        LM,HM,LF,HF = np.meshgrid(x,x,x,x) # all combinations
    
        LM = LM.ravel() # vector
        HM = HM.ravel()
        LF = LF.ravel()
        HF = HF.ravel()

        # b. calculate utility
        u = self.calc_utility(LM,HM,LF,HF)
    
        # c. set to minus infinity if constraint is broken
        I = (LM+HM > 24) | (LF+HF > 24) # | is "or"
        u[I] = -np.inf
    
        # d. find maximizing argument
        j = np.argmax(u)
        
        opt.LM = LM[j]
        opt.HM = HM[j]
        opt.LF = LF[j]
        opt.HF = HF[j]
        opt.u = self.calc_utility(opt.LM, opt.HM, opt.LF, opt.HF)

        # e. print
        if do_print:
            for k,v in opt.__dict__.items():   #//With all the optimal variables, it will turn into a dictionary and print "variable = number"
                print(f'{k} = {v:6.4f}')

        return opt

    def solve(self,do_print=False):
        """ solve model continously """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()

         # a. objective function (to minimize) 
        def objective_function(x):                               #//x will contain all possible LM,HM,LF,HF
            return -self.calc_utility(x[0], x[1], x[2], x[3]) 
        
        # b. constraints
        cons1 = lambda x: 24 - x[0] - x[1]    #//time spent by male cant be above 24
        cons2 = lambda x: 24 - x[2] - x[3]    #//time spent by female cant be above 24
        constraints = ({'type': 'ineq', 'fun': cons1},
                       {'type': 'ineq', 'fun': cons2})
        bounds = ((0,24), (0,24), (0,24), (0,24))
        
        # c. call solver
        initial_guess = [12, 12, 12, 12]
        sol = optimize.minimize(objective_function,initial_guess,
                                method='SLSQP',bounds=bounds,constraints=constraints)
        
        # d. save
        opt.LM = sol.x[0]
        opt.HM = sol.x[1]
        opt.LF = sol.x[2]
        opt.HF = sol.x[3]
        opt.u = self.calc_utility(opt.LM,opt.HM,opt.LF,opt.HF)

        return opt   

    def solve_wF_vec(self,discrete=False):
        """ solve model for vector of female wages """

        pass

    def run_regression(self):
        """ run regression """

        par = self.par
        sol = self.sol

        x = np.log(par.wF_vec)
        y = np.log(sol.HF_vec/sol.HM_vec)
        A = np.vstack([np.ones(x.size),x]).T
        sol.beta0,sol.beta1 = np.linalg.lstsq(A,y,rcond=None)[0]
    
    def estimate(self,alpha=None,sigma=None):
        """ estimate alpha and sigma """

        pass