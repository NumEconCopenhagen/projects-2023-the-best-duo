from types import SimpleNamespace
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

class optimal_taxation_model:

    def __init__(self):
        par = self.par = SimpleNamespace()

        # a. parameters
        par.alpha = 0.5
        par.kappa = 1.0
        par.nu = 1/(2*16**2)
        par.w = 1.0
        par.tau = 0.3
        par.epsilon = 1.0

        # b. set parameters
        par.sigma = [1.001, 1.5]
        par.rho = [1.001, 1.5]

    def V(self,tau,G,L):
        """Calculates the worker utility given tau, G and L"""
        par = self.par

        # a. Calculate consumption
        C = par.kappa + (1-tau)*par.w*L
        
        # b. Calculate utility
        utility = np.log(C**par.alpha * G**(1-par.alpha))

        # c. calculate disutility
        disutility = par.nu * L**2 / 2

        return utility-disutility

    def optimal_L(self,w,tau):
        """Returns the optimal L for each wage and tau"""
        par = self.par

        # a. calculate the value inside the root
        root = par.kappa**2 + 4*(par.alpha/par.nu)*((1-tau)*w)**2

        # b. calculate numerator
        numerator = -par.kappa + root**(1/2)

        # c. calculate labor
        Labor = numerator / ((1-tau)*w*2)

        return Labor
    
    def optimal_G(self,tau):
        """Returns the optimal G for each tau"""
        par = self.par
        
        # a. calculate G
        G = tau * par.w * self.optimal_L(par.w,tau)

        return G
    
    def optimal_tau(self):
        """Returns the optimal tau"""
        par = self.par

        # a. objective function (negated utility, because we are maximize)
        obj_function = lambda tau: -self.V(tau, self.optimal_G(tau), self.optimal_L(par.w,tau))

        # b. bounds
        bounds = (0,1)

        # c. optimize tau
        sol_tau = optimize.minimize_scalar(obj_function,method="bounded",bounds=bounds)

        return sol_tau
    
    def general_V(self,tau,G,L,set_n):
        """Returns the general V function given a tau, G, L and set_n"""
        par = self.par

        # a. set parameters
        sigma = par.sigma[set_n]
        rho = par.rho[set_n]

        # b. calculate consumption
        C = par.kappa + (1-tau)*par.w*L

        # c. calculate utility
        Utility = (par.alpha*C**((sigma-1)/sigma) + (1-par.alpha)*G**((sigma-1)/sigma))
        Utility = Utility ** (sigma/(sigma-1))
        Utility = (Utility ** (1-rho)) - 1
        Utility /= (1-rho)
        
        # d. calculate disutility
        Disutility = (par.nu*L**(1+par.epsilon)) / (1+par.epsilon)

        return Utility - Disutility

    def general_optimal_L(self,tau,G,set_n):
        """Returns the optimal L for the general V function, given a tau, G, and set_n"""
        par = self.par

        # a. objective function
        obj_function = lambda L: -self.general_V(tau,G,L,set_n)

        # b. bounds
        bounds = (0,24)

        # c. optimize L
        sol_L = optimize.minimize_scalar(obj_function,method="bounded",bounds=bounds)

        return sol_L
    
    def general_optimal_G(self,tau,set_n):
        """Returns the optimal G for the general V function, given a tau and set_n"""
        par = self.par
        
        # a. objective function
        obj_function = lambda G: G - tau*par.w*self.general_optimal_L(tau,G,set_n).x

        # b. optimize G
        sol_G = optimize.root_scalar(obj_function,method="brentq",bracket=[0,20])

        return sol_G 
    
    def general_optimal_tau(self,set_n):
        """Returns the optimal tau for the general V function, given a set_n"""
        par = self.par

        # a. objective function
        def obj_function(tau):
            G = self.general_optimal_G(tau,set_n).root
            L = self.general_optimal_L(tau,G,set_n).x
            return -self.general_V(tau,G,L,set_n)
        
        # b. bounds
        bounds = (0,1)

        # c. optimize tau
        sol_tau = optimize.minimize_scalar(obj_function,bounds=bounds,method="bounded")

        return sol_tau
