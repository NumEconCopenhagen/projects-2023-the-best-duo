from HouseholdSpecializationModel import HouseholdSpecializationModelClass
import numpy as np


def loop_alpha_sigma(alpha_vec,sigma_vec):
    """Returns the ratio of HF over HM using all possible values of alpha and sigma, using the discrete model"""
    
    # a. setting parameters
    model = HouseholdSpecializationModelClass()
    sol_array = np.zeros((len(alpha_vec),len(sigma_vec)))

    # b. looping all the values of alpha and sigma
    for alp_i in range(len(alpha_vec)):
        for sig_i in range(len(sigma_vec)):
            model.par.alpha = alpha_vec[alp_i]
            model.par.sigma = sigma_vec[sig_i]
            
            # c. solve
            opt = model.solve_discrete()

            # d. filter out whenever HM is 0 (ratio would be infinite)
            if opt.HM == 0:
                ratio = np.inf
            else:
                ratio = opt.HF / opt.HM
            
            # e. print out results
            print(f'(\u03B1, \u03C3) : ({alpha_vec[alp_i]:.2f}, {sigma_vec[sig_i]:.2F}) --> ratio ={ratio: .4F}')