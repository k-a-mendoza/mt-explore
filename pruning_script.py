#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 13:38:57 2019

@author: kevin
"""

import pandas as pd

df = pd.read_csv('included_stations_all.csv')

#%%
df = df[['project','station','latitude','longitude']]
#%%
df = df.reset_index()
#%%
df.to_csv('potential_backbones.csv')
#%%
df