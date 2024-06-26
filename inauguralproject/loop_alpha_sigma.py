from HouseholdSpecializationModel import HouseholdSpecializationModelClass
import numpy as np


def loop_alpha_sigma(alpha_vec,sigma_vec):
    """Returns the ratio of HF over HM using all possible values of alpha and sigma, using the discrete model"""
    
    # a. setting parameters
    model = HouseholdSpecializationModelClass()
    alpha_array = np.empty((len(alpha_vec),len(sigma_vec)))
    sigma_array = np.empty((len(alpha_vec),len(sigma_vec)))
    ratio_array = np.empty((len(alpha_vec),len(sigma_vec)))

    # b. looping all the values of alpha and sigma
    for alp_i in range(len(alpha_vec)):
        for sig_i in range(len(sigma_vec)):
            model.par.alpha = alpha_vec[alp_i]
            model.par.sigma = sigma_vec[sig_i]
            
            # i. solve
            opt = model.solve_discrete()

            # ii. filter out whenever HM is 0 (ratio would be infinite)
            if opt.HM == 0:
                ratio = np.inf
            else:
                ratio = opt.HF / opt.HM
            
            # iii. print out results
            print(f'(\u03B1, \u03C3) : ({alpha_vec[alp_i]:.2f}, {sigma_vec[sig_i]:.2F}) --> ratio ={ratio: .4F}')

            alpha_array[alp_i,sig_i] = alpha_vec[alp_i]
            sigma_array[alp_i,sig_i] = sigma_vec[sig_i]
            ratio_array[alp_i,sig_i] = ratio
    
    return alpha_array, sigma_array, ratio_array