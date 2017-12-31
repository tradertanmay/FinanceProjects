# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 10:42:26 2017

@author: tanmay
"""

import pandas as pd
import datetime
from coinmarketcap import Market
from pandas import ExcelWriter as ew


coi = Market()

coins_list=[]
for coin in coi.ticker():
    coins_list.append(coin['symbol'])
    
print(coins_list[:5])

print(len(coins_list))

start = pd.to_datetime('now')

usd_price={}
usd_vol={}

t=3

while ((pd.to_datetime('now')- start < datetime.timedelta(minutes=t))):
    if(datetime.datetime.now().time().second%60.0==0):
        s= coi.ticker()
        
        
        
k = pd.to_datetime('now')
stamp_usd={}
stamp_vol={}
for c in range(len(coins_list)):
    if coi.ticker()[c]['price_usd']!=None:
        stamp_usd[coins_list[c]]=float(coi.ticker()[c]['price_usd'])
    else:
        stamp_usd[coins_list[c]]=0
    if coi.ticker()[c]['24h_volume_usd']!=None:
        stamp_vol[coins_list[c]]\
                 =float(coi.ticker()[c]['24h_volume_usd'])
    else:
        stamp_vol[coins_list[c]]=0
        
usd_price[k]=stamp_usd
usd_vol[k]=stamp_vol

a = pd.DataFrame(usd_vol).transpose

df = pd.DataFrame(usd_vol)
writer = pd.ExcelWriter('Tanmay.xlsx',engine='xlsxwriter')


df.to_excel(writer, sheet_name='Sheet1')
writer.save

b = pd.DataFrame(usd_price).transpose
print(a)






        
    