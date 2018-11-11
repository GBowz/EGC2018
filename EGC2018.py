#!/usr/bin/env python
# coding: utf-8

# In[235]:

import matplotlib.pyplot as plt
import requests
import pandas
import matplotlib.patches as mpatches
import pandas as pd
from math import sqrt
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
def get_instrument_prices(instrument_id):
    '''
    Gets the price database for an instrument ID.

    Args:
        instrument_id (int): The ID of the instrument.

    Returns:
        (Series): The list of prices for every epoch for an instrument ID.
    '''
    id_data = requests.get(
        'http://egchallenge.tech/marketdata/instrument/'+str(instrument_id)).json()
    return pandas.DataFrame(id_data)["price"]

# def supplement_prices(existing_prices, current_epoch, IDs, Sym_List):
#     if IDs[0] in existing_prices:
#         if 

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
        'http://egchallenge.tech/marketdata/instrument/'+str(IDs[0])).json()
    #pricedata=[json["price"] for json in id_data]
    Name = Sym_List[0]
    Price_df = pandas.DataFrame({Name: pandas.DataFrame(id_data)["price"]})

    for i in range(1, len(IDs)):
        id_data = requests.get(
            'http://egchallenge.tech/marketdata/instrument/'+str(IDs[i])).json()
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
    # for i in range(len(IDs)):
    plt.plot(Price_df)

    plt.ylabel("Prices")
    plt.xlabel("Epoch")
    plt.legend(Sym_List)
    plt.show()


def get_instrument_SMA(instrument_price_list, time_window):
    '''
    Gets a dictionary of simple moving averages for every time_window epochs.

    Args:
        instrument_price_list (list): A list of prices for every instrument ID.
        time_window (int): The amount of epochs to consider for the moving average.

    Returns:
        (dict) Key: (int) epoch, Value: (float) average
    '''
    running_price_list = {}
    # Iterate through every epoch for a particular instrument symbol
    instrument_epoch_iterator = 0
    number_of_epochs = len(instrument_price_list)

    running_deviation_list = {}
    running_deviation_counter = -1
    exponential_moving_average = 0
    exponential_weighted_standard_deviation = 0

    last_epoch_price = -2
    returns = []

    while (instrument_epoch_iterator < number_of_epochs):
        running_total = 0
        # TODO: The epoch price might return None eventually, we need to fix this.
        running_total_counter = 0
        current_running_deviation = []
        for time_window_iterator in range(time_window):
            if (instrument_epoch_iterator >= number_of_epochs):
                break
            try:
                epoch_price = instrument_price_list[instrument_epoch_iterator]
                running_total += epoch_price

                if last_epoch_price == -2:
                    last_epoch_price = epoch_price
                else:
                    returns.append((epoch_price / last_epoch_price) - 1)

                alpha_decay = 1 - ((number_of_epochs - instrument_epoch_iterator) / number_of_epochs)
                if (exponential_moving_average == 0):
                    exponential_moving_average = epoch_price
                else:
                    exponential_moving_average = alpha_decay * epoch_price + (1 - alpha_decay) * exponential_moving_average

                if (running_deviation_counter > -1):
                    difference = epoch_price - running_price_list[list(running_price_list.keys())[-1]]
                    difference *= difference
                    exponential_weighted_standard_deviation = alpha_decay * sqrt(difference) + (1 - alpha_decay) * exponential_weighted_standard_deviation
                    current_running_deviation.append(difference)
            except:
                pass
            instrument_epoch_iterator += 1
            running_total_counter += 1
        running_total /= running_total_counter + 1

        if len(current_running_deviation) > 0:
            running_variance = 0
            for squared_number in current_running_deviation:
                running_variance += squared_number
            running_variance /= len(current_running_deviation)
            standard_deviation = sqrt(running_variance)

            running_deviation_list[instrument_epoch_iterator] = standard_deviation

        running_deviation_counter += 1
        running_price_list[instrument_epoch_iterator] = running_total

    returns = pandas.Series(returns).autocorr(time_window)

    return running_price_list, running_deviation_list, exponential_moving_average, exponential_weighted_standard_deviation, returns


# In[277]:
def calculate_instrument_SMA(instrument_id, id_symbol, price_df, time_window):
    '''
    Calculates the simple moving average for an instrument ID.

    Args:
        instrument_id (int): The ID of the instrument to calculate SMA for.
        id_symbol (string): The symbol of the instrument.
        price_df (DataFrame): The data frame containing the prices for all epochs of the provided instrument.
        time_window (int): The amount of epochs to consider for the moving average.

    Returns:
        (dict): A dictionary of key (epoch) and value (average after time_window amounts of epochs considered).
    '''
    running_price_list = {}
    # Iterate through every epoch for a particular instrument symbol
    instrument_epoch_iterator = 0
    number_of_epochs = len(price_df[id_symbol])
    while (instrument_epoch_iterator < number_of_epochs):
        running_total = 0
        # TODO: The epoch price might return None eventually, we need to fix this.
        running_total_counter = 0
        for time_window_iterator in range(time_window):
            if (instrument_epoch_iterator >= number_of_epochs):
                break
            epoch_price = price_df[id_symbol][instrument_epoch_iterator]
            running_total += epoch_price
            instrument_epoch_iterator += 1
            running_total_counter += 1
        running_total /= running_total_counter + 1

        running_price_list[instrument_epoch_iterator] = running_total

    return running_price_list


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

        running_price_list = calculate_instrument_SMA(
            instrument_id, id_symbol, price_df, time_window)

        associated_series = pandas.Series(running_price_list)
        new_sma_data_frame = pandas.DataFrame({id_symbol: associated_series})
        sma_data_frame = sma_data_frame.append(new_sma_data_frame)

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

# def create_EMA_Dataframe ():

#     All_EMA = []

#     for i in range(len(IDs)):
#         Price_List = Price_df[Sym_List[i]]
#         EMA_PL = [Price_List[0]]

#         for i in range(1, len(Price_List)):
#             EMA_PL.append(0.5*Price_List[i]+(1-0.5)*EMA_PL[i-1])
#         All_EMA.append(EMA_PL)

#     EMA_P_DF = pandas.DataFrame(All_EMA).T

#     print(EMA_P_DF[::60])
#     return EMA_P_DF[::60]


# EMA_DF = create_EMA_Dataframe()

# def EMA_graph(IDs, Sym_List):

#     for i in range(len(IDs)):
#         plt.plot(EMA_DF)

#         plt.ylabel("Prices")
#         plt.xlabel("Epoch")
#     plt.legend(Sym_List)
#     plt.show()

# EMA_graph(IDs, Sym_List)


if __name__ == "__main__":
    IDs = Firm_ID()
    Sym_List = Line_Names(IDs)
    Price_df = Prices(IDs, Sym_List)
    averages_60 = create_SMA_data_frame(IDs, Sym_List, 60, Price_df)
    show_SMA_graph(averages_60, Sym_List)
