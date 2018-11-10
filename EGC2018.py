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
    N_ID = int(input("How many firms do you want to plot? "))
    IDs=[]
    for i in range(N_ID):
        IDs.append(input("Enter ID of the Firm: "))
    return IDs
IDs = Firm_ID()


# In[279]:


def Line_Names(IDs):
    marketdata = requests.get('http://egchallenge.tech/instruments').json()
    StacD = pandas.DataFrame(marketdata)
    All_Sym_List = StacD["symbol"].tolist()
    Sym_List=[]
    for i in range(len(IDs)):
        Sym_List.append(All_Sym_List[int(IDs[i])-1])

    return Sym_List
        
    
    
Sym_List = Line_Names(IDs)
    


# In[280]:


def Prices(IDs, Sym_List):
    
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

