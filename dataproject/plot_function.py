import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_func(df, country, data):
    """Will plot the dataframe on a normal plot"""

    # a. taking out the desired country's information
    country_data = df[df['country'] == country]
    
    # b. create a plot
    fig, ax1 = plt.subplots()

    # c. set up net migration plot
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Net Migration', color=color)
    ax1.plot(country_data['year'], country_data['Net Migration'], color=color)

    # d. set up other data axis
    ax2 = ax1.twinx()  

    # e. set up other data plot
    color = 'tab:purple'
    ax2.set_ylabel(data, color=color)  
    ax2.plot(country_data['year'], country_data[data], color=color)
    
    # f. final touches and show
    plt.title(f'{country} Net Migration and {data} over Time')
    fig.tight_layout()  
    plt.show()

def scatter_func(df, country, data):
    """Will plot the dataframe on a scatter plot"""

    # a. taking out the desired country's information
    country_data = df[df['country'] == country]
    
    # b. create a plot
    fig, ax1 = plt.subplots()

    # c. set up net migration scatter plot
    color = 'tab:blue'
    ax1.set_xlabel('Net Migration', color = color)
    ax1.set_ylabel(str(data), color = color)
    ax1.scatter(country_data['Net Migration'], country_data[data], color = color)
    
    # d. calculate trend line and plot it
    slope, intercept = np.polyfit(country_data['Net Migration'],country_data[data],1)
    ax1.plot(country_data['Net Migration'],country_data['Net Migration']*slope+intercept)

    # e. final touches and show
    plt.title(f'{country} Net Migration and {data} over Time')
    fig.tight_layout()  
    plt.show()

def plot(df, function):
    """It will plot the variables according to a function (plot_func or scatter_func)"""

    # a. create fixed variable
    fixed_df = widgets.fixed(df)
    
    # b. create changeable variables
    country_widget = widgets.Dropdown(options=df['country'].unique(), description='Country:')
    data_list=df.columns.tolist()[3:]
    data_widget = widgets.Dropdown(options=data_list, description='Data:')

    # c. create an interactive plot
    widgets.interact(function, df=fixed_df, country=country_widget, data=data_widget)