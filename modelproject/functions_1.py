import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from class_1 import economy_simulation

def trade(buyer,seller,do_print=False):
    """
    Will make an interaction between a buyer and a seller in the goods market.
    """
    
    # a. absolute boundaries of price
    max_p = buyer.max_p
    min_p = seller.min_p

    # b. price expected by the buyer  
    p_buyer = min(buyer.curr_p,max_p)
    buyer.curr_p = p_buyer

    # c. price set by the seller
    p_seller = max(seller.curr_p,min_p)
    seller.curr_p = p_seller

    # d. result
    p = np.nan

    # e. successful trade
    if p_seller <= p_buyer and not seller.sold and not buyer.bought:
        
        # i. accounting
        p = p_seller
        buyer.p_curr_surplus = max_p - p_seller
        seller.p_curr_surplus = p_seller - min_p
        buyer.bought = True
        seller.sold = True

        # ii. price adjustments (person decreases and firm increases)
        buyer.curr_p -= 1
        seller.curr_p += 1
    
    # f. print if success
    if do_print and p is not np.nan:
        print(f'The trade was successful, for a price of {p}')
    
    # g. output
    return p


def labor_market(worker,employer,inflation,do_print=False):
    """
    Will make an interaction between a worker and an employer in the labor market.
    """

    # a. absolute boundaries of real wage
    max_rw = employer.max_rw
    min_rw = worker.min_rw

    # b. nominal wage expected by the worker
    w_worker = max(worker.curr_w, int(min_rw*inflation)+1)
    worker.curr_w = w_worker

    # c. nominal wage set by the employer
    w_employer = min(employer.curr_w, int(max_rw*inflation))
    employer.curr_w = w_employer

    # d. result
    w = np.nan

    # e. sucessful interaction
    if  w_worker <= w_employer and not employer.employed and not worker.worked:
        
        # i. accounting
        w = w_employer
        worker.rw_curr_surplus = w - min_rw*inflation
        employer.rw_curr_surplus = max_rw*inflation - w
        employer.employed = True
        worker.worked = True

        # ii. wage adjustments (person increases and firm decreases)
        employer.curr_w -= 1
        worker.curr_w += 1
        
    # f. print if success
    if do_print and w is not np.nan:
        print(f'The trade was successful {employer.id}, for a wage of {w} (real wage: {w/inflation})')

    # g. output
    return w

def plot_func(p_dem_func=None, p_sup_func=None,initial_p=None, rw_dem_func=None, rw_sup_func=None, initial_w=None , n_days=30, n_persons=25, n_firms=25,only_goods=False,only_labor=False):
    """
    Will plot the desired markets' results according to our model.
    It has the same inputs as the class economy_simulation
    """

    # a. simulate economy
    par = economy_simulation(p_dem_func, p_sup_func,initial_p, rw_dem_func, rw_sup_func, initial_w, n_days, n_persons, n_firms,only_goods,only_labor).simulation()
    
    # b. choose the correct unpacking
    if only_goods:
        price,g_demand, g_supply = par
    elif only_labor:
        wage, l_demand, l_supply = par
        price = [initial_p for i in range(n_days)]
    else:
        price,g_demand, g_supply, wage, l_demand, l_supply = par
    
    # c. create figure and subplots
    fig, axs = plt.subplots(2,2)

    r = 0
    # d. if the goods market is allowed
    if not only_labor:
        
        # i. plotting
        axs[r,0].plot(range(n_days),price,color="darkcyan",alpha=0.7)
        axs[r,1].plot(range(n_days),g_demand,color="red",alpha=0.7)
        axs[r,1].plot(range(n_days),g_supply,color="darkcyan",alpha=0.7)

        # ii. setting tittles
        axs[r,0].set_title("Price")
        axs[r,1].set_title("Demand and Supply")
        
        # iii. adding legends
        axs[r,1].legend(["Demand", "Supply"],fontsize=6)

        # iv. setting the y-label
        axs[r,0].set_ylabel("p",rotation="horizontal",fontweight='bold')
        axs[r,1].set_ylabel("Q",rotation="horizontal",fontweight='bold')
    
        # v. setting the x-label
        axs[r,0].set_xlabel("Day",rotation="horizontal",fontweight='bold')
        axs[r,1].set_xlabel("Day",rotation="horizontal",fontweight='bold')
        r += 1

    if not only_goods:
        
        # i. calculate real wage array
        rw = np.array(wage)/np.array(price)

        # ii. plotting
        axs[r,0].plot(range(n_days),wage,color="red",alpha=0.7)
        axs[r,1].plot(range(n_days),l_demand,color="red",alpha=0.7)
        axs[r,1].plot(range(n_days),l_supply,color="darkcyan",alpha=0.7)
        ax = axs[r,0].twinx() 
        ax.plot(range(n_days),rw,color="darkcyan",alpha=0.7)
        
        # iii. setting tittles
        axs[r,0].set_title("Real and Nominal wage")
        axs[r,1].set_title("Demand and Supply")
        
        # iv. adding legends
        axs[r,1].legend(["Labor Demand","Labor Supply"],fontsize=6)
        axs[r,0].legend(["Nominal Wage"],fontsize=6,loc="upper left")
        ax.legend(["Real wage"],loc="lower right",fontsize=6)

        # v. setting the y-label
        axs[r,0].set_ylabel("nw",rotation="horizontal",fontweight='bold')
        axs[r,1].set_ylabel("Q",rotation="horizontal",fontweight='bold')
        ax.set_ylabel("rw",rotation="horizontal",fontweight='bold')
        
        # vi. setting the x-label
        axs[r,0].set_xlabel("Day",rotation="horizontal",fontweight='bold')
        axs[r,1].set_xlabel("Day",rotation="horizontal",fontweight='bold')
    
    if only_goods or only_labor:
        fig.delaxes(axs[1,0])
        fig.delaxes(axs[1,1])

    # e. show the plot
    plt.tight_layout()
    plt.show()

def stand_func(ab, n_persons=None, n_firms=None, dem=False, sup=False):
    """
    Creates a function based on a standardized function.
    The standart function is f(x)=ax+b, where the domain is [0,1].
    Then, it will stretch the function to accomodate for all the agents, either [0,n_persons] or [0,n_firms]
    
    A valid standardized demand function must have f(0)>0 and 0<f(1)<f(0), therefore b>0 and 0<b+a<b.
    A valid standardized supply function must have f(0)>0 and f(1)>f(0), therefore b>0 and a+b>b.
    """

    # a. unpack the slope and intercept
    a, b = ab
    
    # b. choose the right scalar
    if type(n_persons) == int:
        n = n_persons
    elif type(n_firms) == int:
        n = n_firms
    else:
        raise KeyError("n_firms or n_persons must contain an intenger")

    # c. condition for a good demand curve 
    if dem:
        assert a < 0 and b > -a
    
    # d. condition for a good supply curve
    if sup:
        assert a > 0 and b > 0

    # e. create the function, by using the scalar on the standardized function
    def function(x):
        return a*x/n + b
    
    # f. output
    return function

def create_curves(p_dem,p_sup,l_dem,l_sup,n_persons,n_firms,initial_p, initial_w, n_days):
    """
    Will create all the curves and simulate them.
    """
    # a. create all functions
    p_dem_func = stand_func(p_dem, n_persons=n_persons, dem=True)
    p_sup_func = stand_func(p_sup, n_firms=n_firms, sup=True) 
    l_dem_func = stand_func(l_dem, n_firms=n_firms, dem=True)
    l_sup_func = stand_func(l_sup, n_persons=n_persons, sup=True)

    # b. plot the results of the simulation
    plot_func(p_dem_func=p_dem_func, p_sup_func=p_sup_func,initial_p=initial_p, rw_dem_func=l_dem_func, rw_sup_func=l_sup_func, initial_w=initial_w , n_days=n_days, n_persons=n_persons, n_firms=n_firms,only_goods=False,only_labor=False)


def interact():
    """
    Will make an interactive plot.
    """
    # a. create dropdown for the curves
    p_dem = widgets.Dropdown(options=[("steeper",(-80,90)),("normal",(-50,75)),("flatter",(-20,60))],value=(-50,75))
    p_sup = widgets.Dropdown(options=[("steeper",(80,10)),("normal",(50,25)),("flatter",(20,40))],value=(50,25))
    l_dem = widgets.Dropdown(options=[("steeper",(-1.8,1.9)),("normal",(-1,1.5)),("flatter",(-0.2,1.1))],value=(-1,1.5))
    l_sup = widgets.Dropdown(options=[("steeper",(1.8,0.1)),("normal",(1,0.5)),("flatter",(0.2,0.9))],value=(1,0.5))

    # b. create sliders for the parameters
    n_persons = widgets.IntSlider(25, 1, 50)
    n_firms = widgets.IntSlider(25, 1, 50)
    initial_p = widgets.IntSlider(75, 10, 90)
    initial_w = widgets.IntSlider(25, 10, 90)
    n_days = widgets.IntSlider(100, 50, 500, 10)
    
    # c. make them interact within the simulation
    widgets.interact(create_curves, p_dem=p_dem, p_sup=p_sup, l_dem=l_dem, l_sup=l_sup, n_persons=n_persons, n_firms=n_firms, initial_p=initial_p, initial_w=initial_w, n_days=n_days)



    
    