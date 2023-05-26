from types import SimpleNamespace
import numpy as np
import numpy.random as rand
from scipy import optimize

class problem2_model:

    def __init__(self):
        """setup the model"""

        par = self.par = SimpleNamespace()

        # a. set parameters
        par.eta = 0.5
        par.w = 1.0
        par.rho = 0.9
        par.iota = 0.01
        par.sigma_e = 0.1
        par.R = (1+0.01)**(1/12)
        par.l_1 = 0.0
        par.kappa_1 = 1.0
        par.T = 120
        par.delta = 0

    def profit_fun(self,l_t,kappa_t):
        """returns the profit given current labor and kappa"""
        par = self.par

        return kappa_t*l_t**(1-par.eta) - par.w*l_t
    
    def l_t_fun(self,l_t_1, kappa_t):
        """returns current labor with last time labor and current kappa"""
        par = self.par
        
        # a. calculate current labor
        l_t = (((1-par.eta)*kappa_t)/par.w)**(1/par.eta)

        # b. effectively change it if the change is higher than delta
        if abs(l_t - l_t_1) > par.delta:
            return l_t
        
        else:
            return l_t_1
        
        
    
    def epsilon(self):
        """returns a random number from a normal distribution"""
        par = self.par

        return rand.normal(-0.5*par.sigma_e,par.sigma_e)
    
    def k_t_fun(self,kappa_t_1,epsilon):
        """returns a current kappa, with last time kappa and epsilon"""
        par = self.par

        return np.exp(par.rho*np.log(kappa_t_1)+epsilon)
    
    def ex_post(self):
        """returns a value after a shock series"""
        par = self.par
        
        # a. set variables
        t = 0
        value = 0
        l_t_1 = par.l_1
        k_t_1 = par.kappa_1
        epsilon = 0 
        
        # b. iterate until the end of the time series
        while t < par.T:
            
            # i. calculate the kappa and labour
            k_t = self.k_t_fun(k_t_1,epsilon)
            l_t = self.l_t_fun(l_t_1,k_t)
            
            # ii. calculate revenue depending if labor changed or not
            if l_t != l_t_1:
                value += par.R**(-t)*(self.profit_fun(l_t,k_t)-par.iota)

            else:
                value += par.R**(-t)*self.profit_fun(l_t,k_t)

            # iii. prepare variables for next iteration
            t += 1
            k_t_1 = k_t
            l_t_1 = l_t
            epsilon = self.epsilon()
        
        return value
    
    def ex_ante(self,K):
        """Returns the expected value of the salon, simulating K shock series"""
        par = self.par

        # a. set variable
        value = 0

        # b. repeat shock series K times
        for k in range(K):
            value += self.ex_post()
        
        return value/K
    
    def optimize_delta(self,K):
        """Returns the optimal delta, through simulating K shock series"""
        par = self.par

        # a. objective function
        def objective_function(x):
            self.par.delta = x
            return -self.ex_ante(K)
        
        # b. bound
        bound = (0,0.2)

        # c. optimize delta
        sol = optimize.minimize_scalar(objective_function,bounds=bound,method="bounded")

        return sol



        
            

    

