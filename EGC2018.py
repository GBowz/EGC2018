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

IDs = Firm_ID()

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
        
    
    
Sym_List = Line_Names(IDs)
    


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
    id_data = requests.get('http://egchallenge.tech/marketdata/instrument/'+IDs[0]).json()
    #pricedata=[json["price"] for json in id_data]
    Name = Sym_List[0]
    Price_df = pandas.DataFrame({ Name : pandas.DataFrame(id_data)["price"] })
    
    for i in range(1, len(IDs)):
        id_data = requests.get('http://egchallenge.tech/marketdata/instrument/'+IDs[i]).json()
        #pricedata=[json["price"] for json in id_data]
        Name = Sym_List[i]
        Price_df2 = pandas.DataFrame({ Name : pandas.DataFrame(id_data)["price"] })
        Price_df = Price_df.join(Price_df2)
        
    #print(Price_df)
    return Price_df

Price_df = Prices(IDs, Sym_List)


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

graph(IDs, Sym_List)


# In[277]:


def SMA():
    SMA_df = Price_df
    #for i in 

SMA()


# In[ ]:


def SMA_graph(IDs, Sym_List):
    
    for i in range(len(IDs)):
        plt.plot(Price_df)

        plt.ylabel("Prices")
        plt.xlabel("Epoch")
    plt.legend(Sym_List)
    plt.show()

