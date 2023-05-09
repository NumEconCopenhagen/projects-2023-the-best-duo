import numpy as np

def trade(buyer,seller,n_sellers,tol=1,do_print=False):
    max_p = buyer.max_p
    min_p = seller.min_p
    p_buyer = buyer.curr_p
    p_seller = seller.curr_p
    p = np.nan
    success = False

    # a. successful trade
    if p_seller <= p_buyer and not seller.sold and not buyer.bought:
        p = p_seller
        buyer.curr_surplus = max_p - p_seller
        seller.curr_surplus = p_seller- min_p

        #i. price adjustments (agent decreases and firm increases)
        buyer.curr_p -= 1
        seller.curr_p += 1
        buyer.sold = True
        seller.bought = True
    
    elif not buyer.bought:
        buyer.curr_p = min(p_buyer + tol/(n_sellers-1), max_p)
    
    if do_print:
        if p is not np.nan:
            # print('The trade has failed ;-;')
            print(f'The trade was successful, for a price of {p}')
        
    return p