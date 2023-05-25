import numpy as np
from numpy import random as rand
from scipy import optimize
import time

def multistart_optimizer(fun,bounds,tau,K_,K):
    assert tau > 0

    x_k_0_list = []

    for k in range(K):
        # step A
        x_k = rand.uniform(bounds[0],bounds[1],size=2)

        # step b
        if k < K_:
            x_k_0 = x_k

            pass #to step E
            
        else:

            # step c
            Chi_k = 0.5*2/(1+np.exp((k-K_)/100)) 
            
            # step D
            x_k_0 = Chi_k*x_k + (1-Chi_k)*x_star

        # step E
        x_k_star = optimize.minimize(fun,x_k_0,method="BFGS").x

        # step F
        if k == 0 or fun(x_k_star) < fun(x_star):
            x_star = x_k_star
        
        # step G
        if fun(x_star) < tau:
        
            # step 4
            return x_star, x_k_0_list
        
        x_k_0_list.append(x_k_0)



        
        

        

        

