# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 09:42:39 2018

@author: Alex
"""

import requests
import pandas as pd
import statsmodels.formula.api as smf

returns = {}
for n in range(4116, 4127):
    r = requests.get("http://egchallenge.tech/marketdata/epoch/" + str(n))
    returns["epoch_" + str(n)] = pd.DataFrame(r.json())["epoch_return"]

returns = pd.DataFrame(returns)
result = smf.ols("epoch_4126 ~ epoch_4125 + epoch_4124 + epoch_4123", data=returns).fit()

print(result.params)