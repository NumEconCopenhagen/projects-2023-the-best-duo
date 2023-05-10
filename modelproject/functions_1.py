import numpy as np

def trade(buyer,seller,constrained=False,do_print=False):
    max_p = buyer.max_p
    min_p = seller.min_p
        
    p_buyer = min(buyer.curr_p,max_p,buyer.cash)
    buyer.curr_p = p_buyer
    p_seller = max(seller.curr_p,min_p)
    seller.curr_p = p_seller
    p = np.nan

    # a. successful trade
    if (constrained and seller.stock > 0 and buyer.cash >= p_seller) or not constrained:
        if p_seller <= p_buyer and not seller.sold and not buyer.bought:
            p = p_seller
            buyer.p_curr_surplus = max_p - p_seller
            seller.p_curr_surplus = p_seller - min_p

            #i. price adjustments (agent decreases and firm increases)
            buyer.curr_p -= 1
            seller.curr_p += 1
            buyer.bought = True
            seller.sold = True

            if constrained:
                # constraints adjustments
                buyer.cash -= p
                seller.cash += p
                seller.stock -= 1

    else:
        buyer.curr_w += 1
        
    
    if do_print:
        if p is not np.nan:
            # print('The trade has failed ;-;')
            print(f'The trade was successful, for a price of {p}')
    
    return p


def labor_market(worker,employer,inflation,APL=2,constrained=False,do_print=False):
    max_rw = employer.max_rw
    min_rw = worker.min_rw
    w_worker = max(worker.curr_w, int(min_rw*inflation)+1)
    worker.curr_w = w_worker
    w_employer = min(employer.curr_w, int(max_rw*inflation))
    employer.curr_w = w_employer
    w = np.nan
    if (constrained and employer.cash >= w_employer) or not constrained:
        if  w_worker <= w_employer and not employer.employed and not worker.worked:
            w = w_employer
            worker.rw_curr_surplus = w - min_rw*inflation
            employer.rw_curr_surplus = max_rw*inflation - w

            #i. wage adjustments (agent increases and firm decreases)
            employer.curr_w -= 1
            worker.curr_w += 1
            employer.employed = True
            worker.worked = True

            if constrained:
                # constraints adjustments
                employer.cash -= w
                worker.cash += w
                employer.stock += APL
    else:
        employer.curr_p += 1

    if do_print:
        if w is not np.nan:
            # print('The trade has failed ;-;')
            print(f'The trade was successful {employer.id}, for a wage of {w} (real wage: {w/inflation})')

    return w