#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:38:57 2019

@author: kevin
"""

import pandas as pd

df = pd.read_csv('database.csv')

#%%
df = df.loc[df.index[df['include']==1]]
#%%
df.to_csv('database.csv')