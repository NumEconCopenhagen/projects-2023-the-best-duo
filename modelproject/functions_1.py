import numpy as np

def trade(agent,firm,do_print=False):
    max_p = agent.max_p
    min_p = firm.min_p
    p = np.nan

    # a. successful trade
    if max_p >= min_p:
        p = (max_p + min_p)//2
        agent.cash -= p
        firm.cash += p

        #i. price adjustments (agent decreases and firm increases)
        agent.max_p += (p - max_p)//2 
        firm.min_p += (p - min_p)//2
        
    # b. failed trade
    else:

        # i. price adjustments (agent increases and firm decreases)
        agent.max_p += (min_p - max_p)//2 + 1 #without this, the costumer will never go above the min_p (int rounds the value down)
        firm.min_p += (max_p - min_p)//2
    
    if do_print:
        if p is np.nan:
            print('The trade has failed ;-;')
        else:
            print(f'The trade was successful, for a price of {p}')
        
    return p