import ipywidgets as widgets
import matplotlib.pyplot as plt
import pandas as pd

def plot_func(df, country, data):
    country_data = df[df['country'] == country]
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Net migration', color=color)
    ax1.plot(country_data['year'], country_data['net migration'], color=color)
    

    ax2 = ax1.twinx()  

    color = 'tab:purple'
    ax2.set_ylabel(data, color=color)  
    ax2.plot(country_data['year'], country_data[data], color=color)
    

    plt.title(f'{country} Net Migration and gdp over Time')
    fig.tight_layout()  
    plt.show()

def plot(df):
    country_widget = widgets.Dropdown(options=df['country'].unique(), description='Country:')
    data_list=df.columns.tolist()[3:]
    data_widget = widgets.Dropdown(options=data_list, description='Data:')
    widgets.interact(plot_func,df=df, country=country_widget, data=data_widget);

def scatter_func(country, data):
    country_data = wb[wb['country'] == country]
    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Net migration')
    ax1.set_ylabel('Data', color=color)
    ax1.scatter(country_data['net migration'], country_data[data], color=color)
    
    slope, intercept = np.polyfit(country_data['net migration'],country_data[data],1)
    ax1.plot(country_data['net migration'],country_data['net migration']*slope+intercept)

    plt.title(f'{country} Net Migration and data over Time')
    fig.tight_layout()  
    plt.show()