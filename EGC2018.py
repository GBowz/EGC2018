#!/usr/bin/env python
# coding: utf-8

# In[235]:

import matplotlib.pyplot as plt
import requests
import pandas
import matplotlib.patches as mpatches
import pandas as pd

# In[278]:


def Firm_ID():
    '''
    Requests the amount of firms a user wants to plot, requesting the IDs of each
    individual plot after.

    Returns:
        (list) The Firm IDs the user wants.
    '''
    number_of_ids = int(input("How many firms do you want to plot? "))

    IDs = []
    for i in range(number_of_ids):
        IDs.append(input("Enter ID of the Firm: "))

    return IDs

# In[279]:


def Line_Names(IDs):
    '''
    Makes a GET request to the instruments page and returns the symbols of all available instruments.

    Args:
        IDs (list): A list of all instrument IDs.

    Returns:
        (list) The symbols of all instruments.
    '''
    marketdata = requests.get('http://egchallenge.tech/instruments').json()
    StacD = pandas.DataFrame(marketdata)
    All_Sym_List = StacD["symbol"].tolist()
    Sym_List = []
    for i in range(len(IDs)):
        Sym_List.append(All_Sym_List[int(IDs[i])-1])

    return Sym_List


# In[280]:


def Prices(IDs, Sym_List):
    '''
    Makes a GET request and returns the prices of all supplied 

    Args:
        IDs (list): List of IDs of the prices to request.
        Sym_List (list): List of symbols that map to the list argument of IDs.

    Returns:
        (DataFrame): A table of IDs and prices combined together.
    '''
    id_data = requests.get(
        'http://egchallenge.tech/marketdata/instrument/'+IDs[0]).json()
    #pricedata=[json["price"] for json in id_data]
    Name = Sym_List[0]
    Price_df = pandas.DataFrame({Name: pandas.DataFrame(id_data)["price"]})

    for i in range(1, len(IDs)):
        id_data = requests.get(
            'http://egchallenge.tech/marketdata/instrument/'+IDs[i]).json()
        #pricedata=[json["price"] for json in id_data]
        Name = Sym_List[i]
        Price_df2 = pandas.DataFrame(
            {Name: pandas.DataFrame(id_data)["price"]})
        Price_df = Price_df.join(Price_df2)

    # print(Price_df)
    return Price_df


# In[282]:


def graph(IDs, Sym_List):
    '''
    Creates a line graph of epoch against instrument price.

    Args:
        IDs (list): The list of IDs of instruments to use in the graph.
        Sym_List (list): The list of symbols that map to the IDs of the instruments.
    '''
    for i in range(len(IDs)):
        plt.plot(Price_df)

        plt.ylabel("Prices")
        plt.xlabel("Epoch")
    plt.legend(Sym_List)
    plt.show()


# In[277]:


def create_SMA_data_frame(instrument_ids, id_symbols, time_window, price_df):
    '''
    Creates a DataFrame based on the simple moving average of instrument data.

    Args:
        instrument_ids (list): List of instrument IDs.
        id_symbols (list): The mapping of instrument IDs to symbols.
        time_window (int): The window of epochs to use.
        price_df (DataFrame): The data frame of prices in every epoch for every instrument ID.

    Returns:
        (DataFrame): The combination of instrument IDs with a simple moving average of the price.
    '''
    # Initialise DataFrame
    # instrument_id = instrument_ids[0]
    # id_symbol = id_symbols[0]
    sma_data_frame = pandas.DataFrame()

    for i in range(0, len(instrument_ids)):
        instrument_id = instrument_ids[i]
        id_symbol = id_symbols[i]

        running_price_list = []
        # Iterate through every epoch for a particular instrument symbol
        for instrument_epoch_iterator in range(len(price_df[id_symbol])):
            running_total = 0
            # TODO: The epoch price might return None eventually, we need to fix this.
            for time_window_iterator in range(time_window):
                epoch_price = price_df[id_symbol][instrument_epoch_iterator]
                running_total += epoch_price
            running_total /= time_window
            running_price_list.append(running_total)

        new_sma_data_frame = pandas.DataFrame({id_symbol: running_price_list})
        sma_data_frame = sma_data_frame.join(new_sma_data_frame)

    return sma_data_frame


# In[ ]:

def show_SMA_graph(data_frame, id_symbols):
    '''
    Shows a graph of a simple moving average data frame.

    Args:
        data_frame (DataFrame): Instrument symbol as column, SMA price as row.
        id_symbols (list): A string list of symbols that map to each entry of data_frame.
    '''
    plt.plot(data_frame)
    plt.ylabel("Price")
    plt.xlabel("Epoch")
    plt.legend(id_symbols)
    plt.show()


def SMA_graph(IDs, Sym_List):
    for i in range(len(IDs)):
        plt.plot(Price_df)

        plt.ylabel("Prices")
        plt.xlabel("Epoch")
    plt.legend(Sym_List)
    plt.show()


IDs = Firm_ID()
Sym_List = Line_Names(IDs)
Price_df = Prices(IDs, Sym_List)
show_SMA_graph(create_SMA_data_frame(IDs, Sym_List, 10, Price_df), Sym_List)