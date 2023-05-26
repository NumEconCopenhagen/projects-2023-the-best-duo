import numpy as np
from numpy import random as rand
from scipy import optimize

def multistart_optimizer(fun,bounds,tau,K_,K):
    """optimizes the function
    fun: func 
    bounds: list 
    tau: float
    K_: int
        It's the number of warm-up iteractions
    K: int
        It's the total amount of iteractions
    """

    # a. assertions
    assert tau > 0
    assert K_ <= K
    assert bounds[0] < bounds[1]

    # b. start iterations
    x_k_0_list = []

    for k in range(K):
        # i. step A
        x_k = rand.uniform(bounds[0],bounds[1],size=2)

        # ii. step B
        if k < K_:
            x_k_0 = x_k

            pass #to step E
            
        else:

            # 1. step C
            Chi_k = 0.5*2/(1+np.exp((k-K_)/100)) 
            
            # 2. step D
            x_k_0 = Chi_k*x_k + (1-Chi_k)*x_star

        # iii. step E
        x_k_star = optimize.minimize(fun,x_k_0,method="BFGS").x

        # iv. step F
        if k == 0 or fun(x_k_star) < fun(x_star):
            x_star = x_k_star
        
        # v. step G
        if fun(x_star) < tau:
        
            # 1. step 4
            return x_star, x_k_0_list
        
        # vi. append value
        x_k_0_list.append(x_k_0)



        
        

        

        

