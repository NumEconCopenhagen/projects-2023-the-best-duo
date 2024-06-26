
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
        par.rho = 2.0
        par.nuM = 0.001
        par.nuF = 0.001
        par.epsilon = 1.0
        par.omega = 0.5

        # c. household production
        par.alpha = 0.5
        par.sigma = 1.0

        # d. wages
        par.wM = 1.0
        par.wF = 1.0
        par.wF_vec = np.linspace(0.8,1.2,5)

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
            H = ((1-par.alpha)*HM**((par.sigma-1)/par.sigma) + par.alpha*HF**((par.sigma-1)/par.sigma)) ** (par.sigma/(par.sigma-1))

        # c. total consumption utility
        Q = C**par.omega*H**(1-par.omega)
        utility = np.fmax(Q,1e-8)**(1-par.rho)/(1-par.rho)

        # d. disutility of work
        epsilon_ = 1+1/par.epsilon
        TM = LM+HM
        TF = LF+HF
        disutility = par.nuM*(TM**epsilon_/epsilon_) + par.nuF*(TF**epsilon_/epsilon_)
        
        return utility - disutility

    def solve_discrete(self,do_print=False):
        """ solve model discretely """
        
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
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt

    def solve(self,do_print=False):
        """ solve model continously """
        
        opt = SimpleNamespace()

        # a. objective function (to minimize) 
        def objective_function(x):
            return -self.calc_utility(x[0], x[1], x[2], x[3]) * 100 # we made a positive monotone transformation so that the optimization works best
        
        # b. constraints
        cons1 = lambda x: 24 - x[0] - x[1]    #time spent by male can't be above 24
        cons2 = lambda x: 24 - x[2] - x[3]    #time spent by female can't be above 24
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
        opt.u = self.calc_utility(opt.LM,opt.HM,opt.LF,opt.HF) / 100
        
        # e. print
        if do_print:
            for k,v in opt.__dict__.items():
                print(f'{k} = {v:6.4f}')

        return opt   

    def solve_wF_vec(self,method,plot=False):
        """
        Solve model for vector of female wages 
        
        Parameters:
        
        method: func
            It is the method that will be applied to solve the problem.
            It should be "model.solve_discrete" or a "model.solve".
        plot: Bool
            If True, then it will create a plot with the ratios of household production and wages.
        """
        
        par = self.par
        sol = self.sol
        opt = SimpleNamespace()

        # a. solve for all wF values
        for i, wF in enumerate(par.wF_vec):
            par.wF = wF
            
            opt = method()
            sol.LM_vec[i] = opt.LM
            sol.HM_vec[i] = opt.HM
            sol.LF_vec[i] = opt.LF
            sol.HF_vec[i] = opt.HF

        # b. parameter reset
        par.wF = 1

        # c. plot
        if plot:
            
            # i. log the ratios
            logHF_HM = np.log10(sol.HF_vec / sol.HM_vec)
            logwF_wM = np.log10(par.wF_vec / par.wM_vec)

            # ii. plot 
            plt.scatter(logwF_wM, logHF_HM)
            plt.xlabel("log wF/wM",size=15)
            plt.ylabel("log HF/HM",size=15)
            plt.title("log HF/HM against log wF/wM")
            plt.show()   

    def run_regression(self):
        """ run regression """

        par = self.par
        sol = self.sol
    
        x = np.log10(par.wF_vec/par.wM)
        y = np.log10(sol.HF_vec/sol.HM_vec)
        A = np.vstack([np.ones(x.size),x]).T
        sol.beta0,sol.beta1 = np.linalg.lstsq(A,y,rcond=None)[0]
        
        return sol

    def estimate(self,alpha=None):
        par = self.par
        opt = SimpleNamespace()

        # a. objective function (to minimize) 
        def error(x):
            if alpha == None:
                par.alpha = x[0]
            else:
                par.alpha = alpha
            par.sigma = x[1]
            self.solve_wF_vec(self.solve)
            sol = self.run_regression()
            error = (par.beta0_target - sol.beta0)**2 + (par.beta1_target - sol.beta1)**2
            return error * 100
        
        # b. constraints
        bounds = ((0,1), (0,5))
        
        # c. call solver
        initial_guess = [0.5, 1]
        result = optimize.minimize(error,initial_guess, method='Nelder-Mead',bounds=bounds)
        
        # d. save
        if alpha == None:
            opt.alpha = result.x[0]
        else:
            opt.alpha = alpha
        
        opt.sigma = result.x[1]

        par.alpha = opt.alpha
        par.sigma = opt.sigma

        return
    
    def estimate_nu(self):
        par = self.par
        opt = SimpleNamespace()

        # a. objective function (to minimize) 
        def error(x):
            par.sigma = x[0]
            par.nuM = x[1]
            par.nuF = x[2]
            self.solve_wF_vec(self.solve)
            sol = self.run_regression()
            
            error = (par.beta0_target - sol.beta0)**2 + (par.beta1_target - sol.beta1)**2
            return error * 100
        
        # b. constraints
        bounds = ((0,5), (0,1), (0,1))
        
        # c. call solver
        initial_guess = [1.0, 0.01, 0.01]
        result = optimize.minimize(error,initial_guess, method='Nelder-Mead',bounds=bounds)
        
        opt.sigma = result.x[0]
        opt.nuM = result.x[1]
        opt.nuF = result.x[2]

        par.sigma = opt.sigma
        par.nuM = opt.nuM
        par.nuF = opt.nuF

        return opt.sigma, opt.nuM, opt.nuF


        
        

                    
        